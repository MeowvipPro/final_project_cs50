from sentence_transformers import SentenceTransformer
import torch

import faiss
import numpy as np

# Khởi tạo model SentenceTransformer (model embedding) với base model là 'hiieu/halong_embedding' từ hugging face
embedd_model = SentenceTransformer("hiieu/halong_embedding")

# --- Giai đoạn 1: Tạo docs_embedding ---
# Dữ liệu thử nghiệm được lấy từ ví dụ xây dựng RAG system với function calling được chia sẻ tại bài viết: https://viblo.asia/p/quy-trinh-xay-dung-he-thong-rag-tich-hop-function-calling-with-source-code-vlZL98GZJQK
docs = [
    "Xe sedan - thông tin cơ bản: Tên sản phẩm: Toyota Vios G 1.5L AT; Thương hiệu: Toyota; Nhà sản xuất: Toyota Việt Nam; Mã sản phẩm: VIOSG15AT; Loại sản phẩm: Sedan, Xe du lịch; Mô tả ngắn: Sedan nhỏ gọn, thiết kế thời trang, tiết kiệm nhiên liệu, vận hành bền bỉ, phù hợp di chuyển trong thành phố và ngoại ô.",

    "Xe sedan - thông tin chi tiết: - Động cơ: 1.5L Dual VVT-i, xăng. - Hộp số: Tự động 5 cấp. - Mức tiêu thụ nhiên liệu: 5.7L/100km (kết hợp). - Trang bị: Khởi động nút bấm, chìa khóa thông minh, ABS, EBD, camera lùi, màn hình cảm ứng 7 inch. - Màu sắc: Bạc, đen, trắng, đỏ. - Hướng dẫn sử dụng: Thay dầu định kỳ mỗi 5.000 km; đảo lốp sau mỗi 10.000 km.",

    "Xe sedan - thông tin bổ sung: Giá bán: 520.000.000 VNĐ; Tình trạng tồn kho: Còn hàng; Khuyến mãi: Tặng 1 năm bảo hiểm và bộ thảm sàn; Đánh giá của khách hàng: 4.6/5 sao - Lái êm, tiết kiệm nhiên liệu, kiểu dáng thanh lịch.",

    "Xe SUV - thông tin cơ bản: Tên sản phẩm: Mazda CX-5 2.0 Luxury; Thương hiệu: Mazda; Nhà sản xuất: Thaco Auto; Mã sản phẩm: CX520LUX; Loại sản phẩm: SUV, Xe gia đình; Mô tả ngắn: SUV 5 chỗ với thiết kế thể thao, động cơ mạnh mẽ, công nghệ thông minh, thích hợp sử dụng hằng ngày và du lịch.",

    "Xe SUV - thông tin chi tiết: - Động cơ: 2.0L Skyactiv-G, xăng. - Hộp số: Tự động 6 cấp, có chế độ thể thao. - Mức tiêu thụ nhiên liệu: 6.9L/100km (kết hợp). - Trang bị: i-Stop, cruise control, màn hình 10.25 inch, camera 360 độ. - Màu sắc: Xanh đậm, xám, đen, trắng, đỏ. - Hướng dẫn sử dụng: Kiểm tra động cơ mỗi 10.000 km; kiểm tra phanh mỗi 15.000 km.",

    "Xe SUV - thông tin bổ sung: Giá bán: 880.000.000 VNĐ; Tình trạng tồn kho: Còn hàng; Khuyến mãi: Giảm 30 triệu VNĐ và miễn phí bảo dưỡng lần đầu; Đánh giá của khách hàng: 4.8/5 sao - Nội thất rộng, sang trọng, lái đầm chắc.",

    "Xe bán tải - thông tin cơ bản: Tên sản phẩm: Ford Ranger Wildtrak 2.0 Bi-Turbo; Thương hiệu: Ford; Nhà sản xuất: Ford Việt Nam; Mã sản phẩm: RANGERWILD20BT; Loại sản phẩm: Xe bán tải; Mô tả ngắn: Xe bán tải cao cấp, công nghệ hiện đại, khả năng off-road mạnh mẽ, thiết kế nam tính.",

    "Xe bán tải - thông tin chi tiết: - Động cơ: 2.0L Bi-Turbo diesel. - Hộp số: Tự động 10 cấp. - Hệ dẫn động: 4 bánh toàn thời gian. - Trang bị: Cruise control chủ động, hỗ trợ giữ làn đường, màn hình 12 inch, Apple CarPlay không dây. - Màu sắc: Cam, đen, trắng, bạc. - Hướng dẫn sử dụng: Thay lọc dầu diesel mỗi 10.000 km; kiểm tra gầm xe nếu đi địa hình xấu.",

    "Xe bán tải - thông tin bổ sung: Giá bán: 1.160.000.000 VNĐ; Tình trạng tồn kho: Còn hàng; Khuyến mãi: Tặng nắp thùng cuộn và camera lùi; Đánh giá của khách hàng: 4.9/5 sao - Mạnh mẽ, nhiều công nghệ, phù hợp kinh doanh và du lịch.",

    "Xe điện - thông tin cơ bản: Tên sản phẩm: VinFast VF 5 Plus; Thương hiệu: VinFast; Nhà sản xuất: VinFast; Mã sản phẩm: VF5PLUS; Loại sản phẩm: Xe điện, Xe đô thị; Mô tả ngắn: Hatchback điện giá rẻ, thiết kế nhỏ gọn, tiện lợi di chuyển nội thành, không phát thải.",

    "Xe điện - thông tin chi tiết: - Pin: 37.23 kWh lithium-ion. - Quãng đường: Lên tới 300 km/lần sạc. - Thời gian sạc: Khoảng 5.5 tiếng với sạc AC. - Trang bị: Kết nối thông minh, eSIM, điều khiển qua ứng dụng, cảm biến lùi. - Màu sắc: Vàng, trắng, đỏ, xanh bạc hà, đen. - Hướng dẫn sử dụng: Kiểm tra pin định kỳ 12 tháng; cập nhật phần mềm qua app.",

    "Xe điện - thông tin bổ sung: Giá bán: 458.000.000 VNĐ; Tình trạng tồn kho: Còn hàng; Khuyến mãi: Tặng bộ sạc tại nhà và miễn phí bảo dưỡng 3 năm; Đánh giá của khách hàng: 4.7/5 sao - Thiết kế đẹp, thân thiện môi trường, dễ điều khiển trong thành phố."
]
# Tạo embeddings cho các tài liệu và lưu vào biến docs_embeddings
docs_embeddings = embedd_model.encode(docs)

dimension = docs_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(docs_embeddings))

# --- Giai đoạn 2: Hàm truy xuất tài liệu ---
def retrieve_relevant_docs(query: str, top_k: int = 3) -> str:
    query_embedding = embedd_model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)
    return "\n\n".join([docs[i] for i in I[0]])

from transformers import AutoTokenizer, AutoModelForCausalLM

# Khởi tạo tokenizer và model RAG
tokenizer = AutoTokenizer.from_pretrained("himmeow/vi-gemma-2b-RAG")
model = AutoModelForCausalLM.from_pretrained(
    "himmeow/vi-gemma-2b-RAG",
    device_map="auto",
    torch_dtype=torch.bfloat16
)

# Sử dụng GPU nếu có
if torch.cuda.is_available():
    model.to("cuda")

# Định dạng prompt cho model
prompt = """
### Chat_Bot_Car_Infromation:
{}
"""

# Hàm thực hiện quy trình RAG
def generate_answer(query: str) -> str:
    """
    Thực hiện quy trình Retrieval Augmented Generation (RAG) để trả lời câu hỏi.

    Args:
        query: Câu hỏi cần trả lời.

    Returns:
        Câu trả lời được tạo bởi model RAG.
    """
    # Truy xuất tài liệu liên quan
    relevant_docs = retrieve_relevant_docs(query, top_k=3)
    # Định dạng input text
    input_text = prompt.format(relevant_docs, query, " ")
    # Mã hóa input text thành input ids
    input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=128)
    # Sử dụng GPU cho input ids nếu có
    if torch.cuda.is_available():
        input_ids = input_ids.to("cuda")
        
    # Tạo văn bản bằng model
    outputs = model.generate(
        **input_ids,
        max_new_tokens=128,load_in_4bit=False,
        no_repeat_ngram_size=7,  # Ngăn chặn lặp lại các cụm từ 7 gram
        do_sample=True,   # Kích hoạt chế độ tạo văn bản dựa trên lấy mẫu. Trong chế độ này, model sẽ chọn ngẫu nhiên token tiếp theo dựa trên xác suất được tính từ phân phối xác suất của các token.
        temperature=0.2,  # Giảm temperature để kiểm soát tính ngẫu nhiên
        # early_stopping=True,  # Dừng tạo văn bản khi tìm thấy kết thúc phù hợp
        )
    # Giải mã và trả về kết quả
    return tokenizer.decode(outputs[0])
