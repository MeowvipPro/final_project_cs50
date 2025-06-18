from sentence_transformers import SentenceTransformer
import torch

import faiss
import numpy as np

# Khởi tạo model SentenceTransformer (model embedding) với base model là 'hiieu/halong_embedding' từ hugging face
embedd_model = SentenceTransformer("hiieu/halong_embedding")

# --- Giai đoạn 1: Tạo docs_embedding ---
# Dữ liệu thử nghiệm được lấy từ ví dụ xây dựng RAG system với function calling được chia sẻ tại bài viết: https://viblo.asia/p/quy-trinh-xay-dung-he-thong-rag-tich-hop-function-calling-with-source-code-vlZL98GZJQK
docs = [
    # --- Toyota Corolla Cross ---
    "Toyota Corolla Cross là mẫu SUV đô thị 5 chỗ, thiết kế hiện đại, vận hành êm ái và tiết kiệm nhiên liệu. Xe trang bị công nghệ an toàn Toyota Safety Sense, phù hợp cho cả gia đình và cá nhân sử dụng hàng ngày.",
    "Toyota Corolla Cross sử dụng động cơ xăng 1.8L hoặc hybrid, hộp số CVT mượt mà, tiết kiệm nhiên liệu chỉ khoảng 4.5L/100km cho bản hybrid. Xe có chế độ lái Eco, Sport giúp tùy chỉnh trải nghiệm.",
    "Trang bị nổi bật bao gồm: hệ thống cảnh báo điểm mù, cảnh báo phương tiện cắt ngang khi lùi, ga tự động thích ứng và phanh khẩn cấp tự động. Màn hình giải trí 9 inch, kết nối Apple CarPlay và Android Auto.",
    "Corolla Cross có thiết kế nội thất hiện đại với ghế da, cửa sổ trời, điều hòa tự động 2 vùng. Khoang hành lý rộng rãi 440L, phù hợp đi xa hoặc dùng hằng ngày.",

    # --- Hyundai Creta ---
    "Hyundai Creta là mẫu SUV cỡ nhỏ với thiết kế trẻ trung, nội thất rộng rãi và tiện nghi. Xe trang bị nhiều công nghệ hiện đại như màn hình cảm ứng lớn, camera lùi và hỗ trợ lái an toàn.",
    "Hyundai Creta được trang bị động cơ Smartstream 1.5L kết hợp hộp số iVT, tiết kiệm nhiên liệu khoảng 6.3L/100km. Xe có hệ thống treo tinh chỉnh cho độ êm ái cao.",
    "Creta nổi bật với gói công nghệ an toàn SmartSense gồm hỗ trợ giữ làn, cảnh báo va chạm trước, hỗ trợ tránh va chạm điểm mù. Xe có màn hình kỹ thuật số 10.25 inch.",
    "Nội thất Creta hướng đến người trẻ với ghế bọc da thể thao, đèn viền nội thất, sạc không dây, điều hòa tự động có lọc bụi mịn PM2.5. Khoang ghế sau có cửa gió riêng.",

    # --- Kia Sportage ---
    "Kia Sportage là mẫu SUV 5 chỗ với thiết kế thể thao, mạnh mẽ và không gian nội thất hiện đại. Xe phù hợp cho cả di chuyển trong thành phố lẫn hành trình đường dài nhờ khả năng vận hành ổn định và tiết kiệm nhiên liệu.",
    "Kia Sportage trang bị động cơ 2.0L xăng hoặc diesel, hộp số tự động 6–8 cấp, tuỳ chọn hệ dẫn động AWD. Mức tiêu hao nhiên liệu dao động từ 6.5–7.5L/100km tùy phiên bản.",
    "Hệ thống an toàn ADAS gồm giữ làn, cảnh báo tiền va chạm, phanh khẩn cấp, camera 360 độ, hiển thị thông tin trên kính lái HUD. Xe có chế độ lái địa hình tùy chỉnh.",
    "Nội thất Sportage được thiết kế dạng cong liền mạch với màn hình đôi 12.3 inch, ghế chỉnh điện có sưởi/làm mát, hệ thống âm thanh Harman Kardon cao cấp."
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
Chat_Bot_Car_Infromation:
{}
"""

# Hàm thực hiện quy trình RAG
def generate_answer(query: str) -> str:
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
        max_new_tokens=128,
        no_repeat_ngram_size=7,  # Ngăn chặn lặp lại các cụm từ 7 gram
        do_sample=True,   # Kích hoạt chế độ tạo văn bản dựa trên lấy mẫu. Trong chế độ này, model sẽ chọn ngẫu nhiên token tiếp theo dựa trên xác suất được tính từ phân phối xác suất của các token.
        temperature=0.2,  # Giảm temperature để kiểm soát tính ngẫu nhiên
        # early_stopping=True,  # Dừng tạo văn bản khi tìm thấy kết thúc phù hợp
        )
    # Giải mã và trả về kết quả
    return tokenizer.decode(outputs[0])
