let timeLeft = 600; // 10 minutes in seconds

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    document.getElementById("timer").innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    document.getElementById("progress").value = 600 - timeLeft;
    if (timeLeft <= 0) {
        document.getElementById("exam-form").submit();
    }
    timeLeft--;
}

setInterval(updateTimer, 1000);
