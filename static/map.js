// 1. Khởi tạo bản đồ Leaflet, đặt tâm tại Việt Nam
const map = L.map('map').setView([16.047079, 108.206230], 6); 

// Thêm lớp bản đồ nền miễn phí từ OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Mảng màu sắc ngẫu nhiên để phân biệt lộ trình các shipper
const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6'];

// Lắng nghe sự kiện click nút Tối ưu
document.getElementById('btn-optimize').addEventListener('click', async () => {
    const hour = document.getElementById('hour-select').value;
    
    try {
        // Gọi API Backend Python (Ví dụ dùng FastAPI hoặc Flask)
        const response = await fetch(`/api/optimize?hour=${hour}`);
        const data = await response.json();
        
        renderRoutes(data);
    } catch (error) {
        console.error("Lỗi lấy dữ liệu lộ trình:", error);
    }
});

function renderRoutes(data) {
    // Xóa các nét vẽ cũ nếu có trước khi vẽ mới
    map.eachLayer((layer) => {
        if (!!layer.toGeoJSON && layer !== map) map.removeLayer(layer);
    });
    
    const listContainer = document.getElementById('shipper-list');
    listContainer.innerHTML = ''; // Reset danh sách sidebar

    let colorIndex = 0;

    // Duyệt qua từng shipper trong kết quả trả về từ `multi_shipper.py`
    for (const [shipperId, info] of Object.entries(data)) {
        const color = colors[colorIndex % colors.length];
        colorIndex++;

        // 1. Hiển thị thông tin lên thanh Sidebar
        const card = document.createElement('div');
        card.className = 'shipper-card';
        card.style.borderLeftColor = color;
        card.innerHTML = `
            <strong>Shipper ID: ${shipperId}</strong>
            <p>Thời gian: ${info.total_time_minutes} phút</p>
            <small>Lộ trình: ${info.route.join(' → ')}</small>
        `;
        listContainer.appendChild(card);

        // 2. Vẽ các điểm ghim (Marker) và đường nối (Polyline) trên bản đồ
        const latLngs = [];
        
        info.coordinates.forEach((coord, index) => {
            latLngs.push([coord.latitude, coord.longitude]);

            // Thêm Marker cho từng điểm giao
            L.marker([coord.latitude, coord.longitude])
                .addTo(map)
                .bindPopup(`<b>${coord.city_name}</b><br>Thứ tự đi: ${index}`);
        });

        // Vẽ đường nối lộ trình di chuyển của shipper này
        L.polyline(latLngs, {
            color: color,
            weight: 4,
            opacity: 0.8
        }).addTo(map);
    }
}
