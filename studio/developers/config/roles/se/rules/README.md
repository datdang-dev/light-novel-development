# System & Software Engineering Rules

Thư mục này chứa các quy tắc (rules) dành riêng cho nhánh **`se`** (Kiến trúc sư hệ thống và kỹ sư prompt cấu trúc).

**Định hướng lưu trữ:**

1. **Data Contracts**: Các file cấu trúc JSON, lược đồ schema giao tiếp giữa các agent.
2. **Context Window Limits**: Các rule về tối ưu lượng token, cắt giảm metadata thừa.
3. **Pipeline Flow**: Các rule quy định invariant khi truyền context từ module này qua module khác.
4. **Resiliency**: Tiêu chuẩn xử lý lỗi, circuit breakers khi LLM trả về JSON lỗi.

*Hiện tại thư mục vừa được khởi tạo theo chuẩn mới. Trong các bản cập nhật tới, các file quy chuẩn như `global_rule_hub.md` hoặc `architecture_limits.md` sẽ được migrate dần vào đây.*
