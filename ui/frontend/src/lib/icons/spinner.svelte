<style>
.spinner {
  animation: rotate 2.5s linear infinite;
}

.path {
    stroke: currentColor;
    stroke-linecap: round;
    animation: dash 2s ease-in-out infinite;
  }

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}


</style>

<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="spinner bi" viewBox="0 0 16 16">
  <circle class="path" cx="8" cy="8" r="6" fill="none" stroke-width="3"></circle>
</svg>