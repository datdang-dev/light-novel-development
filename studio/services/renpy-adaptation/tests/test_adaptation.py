#!/usr/bin/env python3
import os
import json
import tempfile
import unittest
import shutil
import sys

# Add project root and local service directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
service_dir = os.path.abspath(os.path.join(script_dir, ".."))
project_root = os.path.abspath(os.path.join(script_dir, "../../../.."))
if service_dir not in sys.path:
    sys.path.insert(0, service_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tools.compile_playthrough_novel import RenPyPlaythroughCompiler, AssetResolutionError, ChoiceResolutionError
from tools.scene_packetizer import ScenePacketizer
from tools.verify_sensory_density import SensoryDensityValidator
from tools.suki_riko_orchestrator import SukiRikoOrchestrator
from schemas import ScreenplayOutput

MOCK_RPY_CONTENT = """
define p = Character("Kensou")
define a = Character("Asuka")

label start:
    $ player_name = "Kensou"
    scene bg school_roof with dissolve
    play music "romantic.mp3"
    show asuka neutral
    a "Chào cậu, Kensou."
    menu:
        "Tỏ tình":
            a "Tớ... tớ cũng thích cậu!"
            show asuka seductive
            a "Hãy làm chuyện đó đi..."
        "Từ chối":
            a "Hừm, đồ ngốc!"
            jump bad_end
            
    return

label bad_end:
    scene bg street
    a "Tạm biệt."
    return
"""

class TestRenPyAdaptation(unittest.TestCase):
    def setUp(self):
        # Create temporary rpy file
        self.rpy_fd, self.rpy_path = tempfile.mkstemp(suffix=".rpy", text=True)
        with open(self.rpy_path, "w", encoding="utf-8") as f:
            f.write(MOCK_RPY_CONTENT)
            
        # Create temporary asset root
        self.asset_root = tempfile.mkdtemp()
        self.images_dir = os.path.join(self.asset_root, "images")
        self.bg_dir = os.path.join(self.images_dir, "bg")
        self.sprites_dir = os.path.join(self.images_dir, "sprites")
        os.makedirs(self.bg_dir, exist_ok=True)
        os.makedirs(self.sprites_dir, exist_ok=True)
        
        with open(os.path.join(self.bg_dir, "school_roof.png"), "w") as f:
            f.write("")
        with open(os.path.join(self.bg_dir, "street.webp"), "w") as f:
            f.write("")
        with open(os.path.join(self.sprites_dir, "asuka_neutral.png"), "w") as f:
            f.write("")
        with open(os.path.join(self.sprites_dir, "asuka_seductive.png"), "w") as f:
            f.write("")

    def tearDown(self):
        # Clean up files
        os.close(self.rpy_fd)
        if os.path.exists(self.rpy_path):
            os.remove(self.rpy_path)
        if os.path.exists(self.asset_root):
            shutil.rmtree(self.asset_root)

    def test_compiler_branching_path_love(self):
        # Route: Tỏ tình
        compiler = RenPyPlaythroughCompiler(
            script_path=self.rpy_path,
            choice_matrix_dict={"choices": {"tỏ tình": "Tỏ tình"}}
        )
        result = compiler.compile("start")
        
        elements = result["screenplay"]
        types = [e["type"] for e in elements]
        
        self.assertIn("scene", types)
        self.assertIn("play_music", types)
        
        dialogues = [e["text"] for e in elements if e["type"] == "dialogue"]
        self.assertIn("Tớ... tớ cũng thích cậu!", dialogues)
        self.assertIn("Hãy làm chuyện đó đi...", dialogues)
        self.assertEqual(result["metadata"]["variables"]["player_name"], "Kensou")

    def test_compiler_branching_path_reject(self):
        # Route: Từ chối
        compiler = RenPyPlaythroughCompiler(
            script_path=self.rpy_path,
            choice_matrix_dict={"choices": {"từ chối": "Từ chối"}}
        )
        result = compiler.compile("start")
        
        elements = result["screenplay"]
        dialogues = [e["text"] for e in elements if e["type"] == "dialogue"]
        
        self.assertIn("Tạm biệt.", dialogues)
        self.assertNotIn("Tớ... tớ cũng thích cậu!", dialogues)
        
        scenes = [e["value"] for e in elements if e["type"] == "scene"]
        self.assertIn("street", scenes)

    def test_compiler_pydantic_schema_validation(self):
        compiler = RenPyPlaythroughCompiler(
            script_path=self.rpy_path,
            choice_matrix_dict={"choices": {"tỏ tình": "Tỏ tình"}}
        )
        result = compiler.compile("start")
        
        # Validates screenplay dict directly
        validated = ScreenplayOutput.model_validate(result)
        self.assertGreater(len(validated.screenplay), 0)
        self.assertEqual(validated.metadata.start_label, "start")

    def test_compiler_asset_resolution_success(self):
        compiler = RenPyPlaythroughCompiler(
            script_path=self.rpy_path,
            choice_matrix_dict={"choices": {"tỏ tình": "Tỏ tình"}},
            asset_root=self.asset_root
        )
        result = compiler.compile("start")
        
        elements = result["screenplay"]
        scene_elem = [e for e in elements if e["type"] == "scene"][0]
        show_elem = [e for e in elements if e["type"] == "show" and e["character"] == "Asuka"][0]
        
        self.assertEqual(scene_elem["asset_path"], "images/bg/school_roof.png")
        self.assertEqual(show_elem["asset_path"], "images/sprites/asuka_neutral.png")

    def test_compiler_asset_resolution_missing(self):
        with tempfile.TemporaryDirectory() as empty_dir:
            compiler = RenPyPlaythroughCompiler(
                script_path=self.rpy_path,
                choice_matrix_dict={"choices": {"tỏ tình": "Tỏ tình"}},
                asset_root=empty_dir
            )
            with self.assertRaises(AssetResolutionError):
                compiler.compile("start")

    def test_scene_packetizer(self):
        compiler = RenPyPlaythroughCompiler(
            script_path=self.rpy_path,
            choice_matrix_dict={"choices": {"tỏ tình": "Tỏ tình"}}
        )
        result = compiler.compile("start")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            screenplay_path = os.path.join(temp_dir, "screenplay.json")
            with open(screenplay_path, "w", encoding='utf-8') as f:
                json.dump(result, f)
                
            packetizer = ScenePacketizer(screenplay_path, max_dialogue_lines=2)
            packets = packetizer.packetize()
            
            self.assertGreater(len(packets), 1)
            self.assertEqual(packets[0]["context_state"]["active_background"], "school_roof")
            self.assertIn("Asuka", packets[0]["context_state"]["present_characters"])

    def test_verify_sensory_density_screenplay(self):
        validator = SensoryDensityValidator()
        packet = {
            "elements": [
                {"type": "scene", "value": "roof", "effects": "dissolve"},
                {"type": "play_music", "value": "music"},
                {"type": "show", "character": "Asuka", "expression": "seductive"},
                {"type": "dialogue", "speaker": "Asuka", "text": "Hội thoại", "vpunch": True}
            ]
        }
        report = validator.verify_screenplay_packet(packet)
        self.assertGreaterEqual(report["sensory_score"], 35)
        self.assertTrue(report["passed"])

    def test_verify_sensory_density_prose(self):
        validator = SensoryDensityValidator()
        
        slop_content = (
            "Asuka nhìn tôi đầy thách thức. Tôi cảm thấy không thể cưỡng lại vẻ đẹp của cô ấy, "
            "một sự pha trộn giữa kiêu kỳ và bí ẩn. Khoảnh khắc định mệnh này làm tôi vừa sợ hãi vừa tò mò."
        )
        report_slop = validator.verify_prose(slop_content)
        self.assertFalse(report_slop["passed"])
        self.assertTrue(any("AI-slop cliché" in c for c in report_slop["critique"]))
        
        premium_content = (
            "Trên sân thượng, hơi thở Asuka dốc lên từng nhịp gấp gáp đầy kích thích. "
            "Làn da nóng ran của nàng áp sát vào lồng ngực tôi, khít khao và ẩm ướt. "
            "Nàng khẽ rùng mình, tiếng rên rỉ khẽ khàng thoát ra từ đôi môi ngọt ngào ấy. "
            "Da thịt chạm nhau tỏa ra hơi ấm nồng nàn khiến nhịp tim cả hai cùng giật bắn thổn thức."
        )
        report_premium = validator.verify_prose(premium_content)
        self.assertTrue(report_premium["passed"])
        self.assertGreaterEqual(report_premium["sensory_score"], 80)

    def test_suki_riko_orchestrator(self):
        compiler = RenPyPlaythroughCompiler(
            script_path=self.rpy_path,
            choice_matrix_dict={"choices": {"tỏ tình": "Tỏ tình"}}
        )
        result = compiler.compile("start")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            screenplay_path = os.path.join(temp_dir, "playthrough_start_screenplay.json")
            with open(screenplay_path, "w", encoding='utf-8') as f:
                json.dump(result, f)
                
            orchestrator = SukiRikoOrchestrator(max_retries=3, mock=True)
            final_chapters = orchestrator.run_pipeline(screenplay_path, temp_dir)
            
            self.assertGreater(len(final_chapters), 0)
            for chapter_file in final_chapters:
                self.assertTrue(os.path.exists(chapter_file))
                with open(chapter_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.assertIn("(Sensory Upgraded)", content)

if __name__ == "__main__":
    unittest.main()
