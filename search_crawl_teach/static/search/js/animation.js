// FIX: THIS CODE IS NOT WORKING, BUT LAUNCHING AND EXECUTING, NEED TO FIND ANSWER


function createBubble(x, y) {
    const bubble = document.createElement("span");
    document.body.appendChild(bubble);

    const size = Math.floor(Math.random() * 100) + 50 + "px";
    const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.8)`;
    const duration = Math.floor(Math.random() * 20) + 10 + "s";

    bubble.style.position = "absolute";
    bubble.style.top = `${y}px`;
    bubble.style.left = `${x}px`;
    bubble.style.display = "block";
    bubble.style.background = color;
    bubble.style.width = size;
    bubble.style.height = size;
    bubble.style.borderRadius = "50%";
    bubble.style.opacity = "0";
    bubble.style.pointerEvents = "none";
    bubble.style.zIndex = "-1";

    bubble.animate([
        { opacity: "0", transform: "scale(0)" },
        { opacity: "0.8", transform: "scale(1)" },
        { opacity: "0", transform: "scale(2)" }
    ], {
        duration: duration,
        easing: "ease-out",
        iterations: 1,
        fill: "forwards"
    });

    setTimeout(() => {
        bubble.remove();
    }, parseInt(duration) * 1000);
}

document.addEventListener("click", function (event) {
    const x = event.clientX;
    const y = event.clientY;

    createBubble(x, y);
});