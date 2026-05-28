import argparse
import asyncio
import logging
import sys
import time
from pathlib import Path
from studio.core.caption_engine.adapters.toriigate_mcp_adapter import ToriigateMCPAdapter
from studio.core.caption_engine.adapters.studio_prompt_loader import StudioPromptLoader
from studio.core.caption_engine.adapters.filesystem_output_repo import FilesystemOutputRepository
from studio.core.caption_engine.adapters.in_process_qwen2vl_adapter import InProcessQwen2VLAdapter

logger = logging.getLogger("caption-engine-orchestrator")

# ── ANSI Terminal Color Constants ────────────────────────────────────────────
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"


class CaptionEngine:
    """Unified Facade for LND Studio Erotic Captioning.

    Coordinates loading of templates, direct vision model execution,
    and simple filesystem persistence. Runs entirely in a single, direct pass.
    """

    def __init__(
        self,
        api_url: str = "http://127.0.0.1:1234",
        workspace_root: str | None = None,
        output_dir: str | None = None,
        mcp_client=None,
    ):
        self.mcp_adapter = mcp_client or ToriigateMCPAdapter(api_url=api_url)
        self.prompt_loader = StudioPromptLoader(workspace_root=workspace_root)
        self.output_repo = FilesystemOutputRepository(output_dir=output_dir)

        # Setup centralized real-time file logging under _lnd-output
        ws = Path(workspace_root or "/home/datdang/working/lnd_dev")
        log_dir = ws / "_lnd-output"
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = log_dir / "caption_engine.log"

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        
        # Configure orchestrator logger
        logger.setLevel(logging.INFO)
        logger.propagate = False
        if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            logger.addHandler(file_handler)

        # Configure adapter logger
        adapter_logger = logging.getLogger("in_process_qwen2vl_adapter")
        adapter_logger.setLevel(logging.INFO)
        adapter_logger.propagate = False
        if not any(isinstance(h, logging.FileHandler) for h in adapter_logger.handlers):
            adapter_logger.addHandler(file_handler)

    async def run(
        self,
        image_path: str,
        mood_seed: str = "AUTO",
        user_context: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.5,
        caption_type: str = "direct_caption",
        stream: bool = True,
    ) -> dict:
        """Run the direct visual captioning pipeline for the target image in a single pass."""
        p = Path(image_path)
        if not p.exists():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        start_time = time.perf_counter()

        # Build start layout (Colored for terminal, uncolored for file log)
        start_border_colored = (
            "\n"
            f"{C_CYAN}┌────────────────────────────────────────────────────────────┐{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}              {C_BOLD}{C_GREEN}CAPTION ENGINE TASK INITIALIZED{C_RESET}               {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Target Image{C_RESET}    : {C_BOLD}{p.resolve()}{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Image Size{C_RESET}      : {p.stat().st_size:,} bytes\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Template Type{C_RESET}   : {C_YELLOW}{caption_type}{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Mood Seed{C_RESET}       : {C_BLUE}{mood_seed}{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Temperature{C_RESET}     : {temperature}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Max Gen Tokens{C_RESET}  : {max_tokens}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Stream Mode{C_RESET}     : {C_GREEN if stream else C_YELLOW}{stream}{C_RESET}\n"
            f"{C_CYAN}└────────────────────────────────────────────────────────────┘{C_RESET}\n"
        )

        logger.info(start_border_colored)
        sys.stdout.write(start_border_colored)
        sys.stdout.flush()

        # ── Direct Visual Caption (Suki) ──────────────────────────
        prompt_start = time.perf_counter()
        compiled_caption_prompt = self.prompt_loader.load_direct_prompt(
            mood_seed=mood_seed, user_context=user_context, prompt_name=caption_type
        )
        prompt_duration = time.perf_counter() - prompt_start

        logger.info(f"Compiled prompt for {p.name}:\n---\n{compiled_caption_prompt}\n---")

        inference_start = time.perf_counter()
        raw_caption = await self.mcp_adapter.generate_caption(
            image_path=image_path,
            compiled_prompt=compiled_caption_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stream_tokens=stream,
        )
        inference_duration = time.perf_counter() - inference_start
        total_duration = time.perf_counter() - start_time

        # Word and character count for statistics
        word_count = len(raw_caption.split())
        char_count = len(raw_caption)

        # Build clean final single-shot report
        report_colored = (
            "\n"
            f"{C_CYAN}┌────────────────────────────────────────────────────────────┐{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}               {C_BOLD}{C_GREEN}CAPTION ENGINE PIPELINE REPORT{C_RESET}               {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_BOLD}{C_YELLOW}[Execution Metrics]{C_RESET}                                       {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Prompt Compile Time{C_RESET} : {C_BOLD}{prompt_duration:.2f}s{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Model Inference Time{C_RESET}: {C_BOLD}{inference_duration:.2f}s{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Total Pipeline Time{C_RESET} : {C_BOLD}{total_duration:.2f}s{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}                                                            {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_BOLD}{C_YELLOW}[Generation Stats]{C_RESET}                                        {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Output Length{C_RESET}       : {char_count} chars ({word_count} words)\n"
            f"{C_CYAN}│{C_RESET}  {C_MAGENTA}• Model Throughput{C_RESET}    : ~{C_BOLD}{word_count / (inference_duration or 1.0):.1f} words/sec{C_RESET}\n"
            f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
            f"{C_CYAN}│{C_RESET}  {C_BOLD}{C_YELLOW}[Generated Content]{C_RESET}                                       {C_CYAN}│{C_RESET}\n"
            f"{C_CYAN}├────────────────────────────────────────────────────────────┤{C_RESET}\n"
            f"{raw_caption.strip()}\n"
            f"{C_CYAN}└────────────────────────────────────────────────────────────┘{C_RESET}\n"
        )

        # Persist colored report to centralized file logger (so tail -f preserves colors!)
        logger.info(report_colored)

        # Print colored report cleanly to standard stdout in a single shot
        sys.stdout.write(report_colored)
        sys.stdout.flush()

        # Save output
        self.output_repo.save_caption(image_path, raw_caption)

        logger.info(f"{C_GREEN}Pipeline completed successfully in Direct mode for {p.name} ✓{C_RESET}")

        return {
            "success": True,
            "caption": raw_caption.strip(),
            "mood_seed": mood_seed,
            "metrics": {
                "compile_time": prompt_duration,
                "inference_time": inference_duration,
                "total_time": total_duration,
                "words": word_count,
                "chars": char_count,
            }
        }


def parse_args():
    parser = argparse.ArgumentParser(description="LND Studio Caption Engine Production CLI")
    parser.add_argument(
        "--image",
        required=True,
        help="Path to the image to caption",
    )
    parser.add_argument(
        "--type",
        default="direct_caption",
        help="Caption prompt template type (e.g. long_thoughts_v2, json, md_comic, short, etc.)",
    )
    parser.add_argument(
        "--mood",
        default="AUTO",
        help="Mood seed (default: AUTO)",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Optional descriptive user context to inject into prompt",
    )
    parser.add_argument(
        "--temp",
        type=float,
        default=0.5,
        help="Inference temperature (default: 0.5)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum generation tokens (default: 4096)",
    )
    parser.add_argument(
        "--no-stream",
        action="store_false",
        dest="stream",
        help="Disable real-time token streaming to stdout and logs, running in single-shot mode.",
    )
    return parser.parse_args()


async def main():
    args = parse_args()
    
    # Configure logging so it does not output duplicate messages to standard stream
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s")

    # In production CLI, run in-process model directly for zero-dependency speed
    adapter = InProcessQwen2VLAdapter(
        model_path="studio/core/caption_engine/models/ToriiGate-0.5_Q4_K_L.gguf",
        mmproj_path="studio/core/caption_engine/models/mmproj_Q8_0.gguf",
        ngl=99,
        n_ctx=16384,
        verbose=False,
    )

    engine = CaptionEngine(mcp_client=adapter)

    try:
        await engine.run(
            image_path=args.image,
            mood_seed=args.mood,
            user_context=args.context,
            max_tokens=args.max_tokens,
            temperature=args.temp,
            caption_type=args.type,
            stream=args.stream,
        )
    except Exception as e:
        print(f"\n{C_RED}❌ Production Engine Error: {e}{C_RESET}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # If run directly as a script, execute production CLI
    asyncio.run(main())
