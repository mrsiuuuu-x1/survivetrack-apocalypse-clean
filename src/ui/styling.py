"""
CSS Styling System for SurviveTrack
Provides post-apocalyptic themed styling for the Gradio interface.
"""

def get_custom_css() -> str:
    """Get the complete custom CSS for SurviveTrack interface."""
    return """
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.gradio-container {
    background: 
        /* Dark overlay for readability */
        linear-gradient(135deg, 
            rgba(20, 15, 10, 0.75) 0%, 
            rgba(30, 25, 15, 0.70) 25%,
            rgba(25, 20, 15, 0.75) 50%,
            rgba(35, 25, 15, 0.70) 75%,
            rgba(20, 15, 10, 0.75) 100%
        ),
        /* Your post-apocalyptic cityscape */
        url('https://i.postimg.cc/YC386F3Y/bg-image.jpg');
    
    background-attachment: fixed;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    font-family: 'Rajdhani', 'Share Tech Mono', monospace;
    color: #d4af37;
    min-height: 100vh;
    position: relative;
}

/* Dust particles effect */
.gradio-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20% 30%, rgba(218, 165, 32, 0.3), transparent),
        radial-gradient(1px 1px at 40% 70%, rgba(205, 133, 63, 0.2), transparent),
        radial-gradient(1px 1px at 90% 40%, rgba(210, 180, 140, 0.3), transparent);
    background-size: 300px 300px, 200px 200px, 400px 400px;
    animation: dust-float 20s linear infinite;
    pointer-events: none;
    z-index: 1;
}

@keyframes dust-float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.gr-button {
    background: linear-gradient(145deg, 
        rgba(139, 69, 19, 0.8) 0%, 
        rgba(160, 82, 45, 0.9) 50%, 
        rgba(101, 67, 33, 0.8) 100%) !important;
    border: 2px solid rgba(218, 165, 32, 0.6) !important;
    color: #f5deb3 !important;
    font-weight: 600 !important;
    font-family: 'Rajdhani', monospace !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.8) !important;
    box-shadow: 
        0 4px 15px rgba(139, 69, 19, 0.4),
        inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transition: all 0.3s ease !important;
}

.gr-button:hover {
    background: linear-gradient(145deg, 
        rgba(160, 82, 45, 0.9) 0%, 
        rgba(218, 165, 32, 0.8) 50%, 
        rgba(139, 69, 19, 0.9) 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 
        0 6px 20px rgba(218, 165, 32, 0.3),
        inset 0 1px 0 rgba(255,255,255,0.2) !important;
}

.gr-textbox {
    background: linear-gradient(135deg, 
        rgba(25, 25, 25, 0.95) 0%, 
        rgba(40, 30, 20, 0.90) 100%) !important;
    border: 2px solid rgba(218, 165, 32, 0.4) !important;
    color: #d4af37 !important;
    font-family: 'Share Tech Mono', monospace !important;
    box-shadow: 
        0 0 20px rgba(218, 165, 32, 0.1),
        inset 0 2px 4px rgba(0,0,0,0.3) !important;
}

.gr-textbox:focus {
    border-color: rgba(218, 165, 32, 0.8) !important;
    box-shadow: 
        0 0 30px rgba(218, 165, 32, 0.2),
        inset 0 2px 4px rgba(0,0,0,0.3) !important;
}

.gr-chatbot {
    background: 
        linear-gradient(135deg, 
            rgba(20, 15, 10, 0.90) 0%, 
            rgba(30, 20, 15, 0.85) 100%
        ) !important;
    border: 1px solid rgba(139, 69, 19, 0.4) !important;
    box-shadow: 
        0 0 30px rgba(139, 69, 19, 0.2),
        inset 0 2px 10px rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(5px) !important;
}

h1, h2, h3 {
    font-family: 'Rajdhani', monospace !important;
    color: #d4af37 !important;
    text-shadow: 0 0 10px rgba(218, 165, 32, 0.4) !important;
}

h1 {
    background: linear-gradient(45deg, 
        #d4af37 0%, 
        #f4e4bc 25%, 
        #daa520 50%, 
        #b8860b 75%, 
        #d4af37 100%) !important;
    background-size: 200% 200% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: title-glow 4s ease-in-out infinite !important;
}

@keyframes title-glow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: linear-gradient(45deg, rgba(20, 15, 10, 0.8), rgba(25, 20, 15, 0.8));
    border-radius: 6px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, rgba(139, 69, 19, 0.8), rgba(160, 82, 45, 0.8));
    border-radius: 6px;
    border: 1px solid rgba(218, 165, 32, 0.3);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, rgba(160, 82, 45, 0.9), rgba(218, 165, 32, 0.8));
}
"""