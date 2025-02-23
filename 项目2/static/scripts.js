const colors = ['#8B0000', '#FF0000', '#FFA500', '#FFFF00', '#006400', '#90EE90', '#ADD8E6', '#00008B', '#E6E6FA', '#800080', '#FFC0CB'];
let colorIndex = 0;

// 切换星标功能
function toggleStar(element) {
    element.classList.toggle('filled');
    const messageDiv = element.closest('.message');
    const topic = messageDiv.getAttribute('data-topic');

    // 如果尚未分配颜色，则为主题分配颜色
    if (!messageDiv.dataset.color) {
        const color = colors[colorIndex % colors.length];
        colorIndex++;
        assignColorToTopic(topic, color);
    }

    // 为相同主题的所有消息切换高亮类
    const messages = document.querySelectorAll(`.message[data-topic="${topic}"]`);
    messages.forEach(msg => msg.classList.toggle('highlighted'));
}

// 为主题分配颜色
function assignColorToTopic(topic, color) {
    const messages = document.querySelectorAll(`.message[data-topic="${topic}"]`);
    messages.forEach(msg => {
        msg.style.backgroundColor = color;
        msg.dataset.color = color;
    });
}

// 显示模态框
function showModal(element) {
    const modal = document.getElementById('modal');
    modal.style.display = 'flex';
    
    const messageDiv = element.closest('.message');
    const topic = messageDiv.getAttribute('data-topic');
    modal.setAttribute('data-topic', topic);
}

// 保存标签
function saveTag() {
    const modal = document.getElementById('modal');
    const topic = modal.getAttribute('data-topic');
    const tagInput = document.getElementById('tagInput');
    const tagValue = tagInput.value;

    // 保存相同主题的所有消息的标签
    const messages = document.querySelectorAll(`.message[data-topic="${topic}"]`);
    messages.forEach(msg => {
        const tooltip = msg.querySelector('.tooltip');
        tooltip.textContent = tagValue;
        tooltip.style.display = 'block';
    });

    // 关闭模态框
    modal.style.display = 'none';
    tagInput.value = '';
}

// 点击外部关闭模态框
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// 悬停显示提示
document.querySelectorAll('.message').forEach(message => {
    message.addEventListener('mouseover', function() {
        const tooltip = this.querySelector('.tooltip');
        if (tooltip.textContent) {
            tooltip.style.display = 'block';
        }
    });
    message.addEventListener('mouseout', function() {
        const tooltip = this.querySelector('.tooltip');
        tooltip.style.display = 'none';
    });
});

// 提交时显示打字指示器
document.getElementById('qaForm').addEventListener('submit', function() {
    document.getElementById('typing-indicator').style.display = 'flex';
});

// 清空对话历史
document.getElementById('clearHistoryButton').addEventListener('click', function() {
    fetch('/clear-chat-history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userId: 'current-user-id' }) // 根据需要替换成实际的用户ID
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('对话历史已清空');
            location.reload();  // 刷新页面以更新对话历史
        } else {
            alert('清空对话历史失败');
        }
    })
    .catch(error => {
        console.error('错误:', error);
        alert('清空对话历史时发生错误');
    });
});
