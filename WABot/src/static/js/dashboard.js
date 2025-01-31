// Check authentication
if (!localStorage.getItem('authToken')) {
    window.location.href = 'login.html';
}

// Sidebar Toggle
document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.querySelector('.sidebar').classList.toggle('active');
});

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('authToken');
    window.location.href = 'login.html';
});

// Fetch Dashboard Data
async function fetchDashboardData() {
    try {
        const response = await fetch('/api/dashboard', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            updateDashboardStats(data);
            updateCharts(data);
        } else {
            console.error('Failed to fetch dashboard data');
        }
    } catch (error) {
        console.error('Dashboard data error:', error);
    }
}

function updateDashboardStats(data) {
    // Update stat cards with real data
    const statCards = document.querySelectorAll('.stat-number');
    // Example: Update first stat card with total students
    if (data.totalStudents) {
        statCards[0].textContent = data.totalStudents;
    }
}

function updateCharts(data) {
    // Implementation for charts will go here
    // You can use a lightweight charting library if needed
}

// Initial load
fetchDashboardData();