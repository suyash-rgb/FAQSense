import React from 'react';
import './Logo.css';

const Logo = ({ className = "" }) => {
    return (
        <div className={`logo-container ${className}`}>
            <div className="logo-icon-wrapper">
                <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="logo-svg">
                    <defs>
                        <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#8B5CF6" />
                            <stop offset="100%" stopColor="#06B6D4" />
                        </linearGradient>
                    </defs>
                    <path
                        d="M20 25C20 25 40 10 75 25C90 32 85 50 65 52C50 54 25 45 20 45V25Z"
                        fill="url(#logo-gradient)"
                    />
                    <path
                        d="M20 50C20 50 35 40 65 52C75 58 75 72 55 75C40 78 25 70 20 70V50Z"
                        fill="url(#logo-gradient)"
                        opacity="0.85"
                    />
                    <path
                        d="M20 75C20 75 30 68 50 78C58 83 55 93 45 95C35 97 25 90 20 90V75Z"
                        fill="url(#logo-gradient)"
                        opacity="0.7"
                    />
                </svg>
            </div>
            <div className="logo-text">
                <span className="logo-faq">FAQ</span><span className="logo-sense">Sense</span>
            </div>
        </div>
    );
};

export default Logo;
