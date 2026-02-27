import React from 'react';
import { Link } from 'react-router-dom';
import {
    SignedIn,
    SignedOut,
    SignInButton,
    SignUpButton,
    UserButton,
} from "@clerk/clerk-react";
import './LandingPage.css';

const Navbar = () => (
    <nav className="navbar">
        <div className="nav-logo">FAQSense<span>.ai</span></div>
        <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#reviews">Reviews</a>
            <a href="#faq">FAQ</a>
            <SignedOut>
                <SignInButton mode="modal">
                    <button className="nav-link-btn">Login</button>
                </SignInButton>
                <SignUpButton mode="modal">
                    <button className="signup-btn">Sign Up</button>
                </SignUpButton>
            </SignedOut>
            <SignedIn>
                <Link to="/dashboard" className="nav-btn">Launch Dashboard</Link>
                <UserButton afterSignOutUrl="/" />
            </SignedIn>
        </div>
    </nav>
);

const Hero = () => (
    <section className="hero">
        <div className="hero-content">
            <div className="badge">Next-Gen Bot Intelligence</div>
            <h1>Power Your FAQ with <span>Robotic Precision</span></h1>
            <p>Instant, accurate, and autonomous support for your customers. FAQSense uses cutting-edge neural flows to handle queries 24/7.</p>
            <div className="hero-actions">
                <Link to="/dashboard" className="primary-btn">Start Building</Link>
                <button className="secondary-btn">Watch Demo</button>
            </div>
        </div>
        <div className="hero-image">
            <div className="abstract-visual-container">
                <div className="robot-glow"></div>
                <div className="abstract-mesh">
                    {[...Array(6)].map((_, i) => (
                        <div key={i} className="mesh-node"></div>
                    ))}
                </div>
            </div>
        </div>
    </section>
);

const Reviews = () => (
    <section id="reviews" className="reviews">
        <h2>Trusted by Industry Giants</h2>
        <div className="reviews-grid">
            <div className="review-card">
                <p>"The robotic flow editor is a game changer for our documentation team."</p>
                <div className="reviewer">
                    <div className="avatar">JD</div>
                    <div>
                        <strong>Jane Doe</strong>
                        <span>TechCorp CEO</span>
                    </div>
                </div>
            </div>
            <div className="review-card">
                <p>"Integration took minutes, and the AI handled 90% of our common tickets instantly."</p>
                <div className="reviewer">
                    <div className="avatar">MS</div>
                    <div>
                        <strong>Mark Smith</strong>
                        <span>Ops Lead @ CloudX</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
);

const FAQ = () => (
    <section id="faq" className="faq">
        <h2>Common Inquiries</h2>
        <div className="faq-list">
            <div className="faq-item">
                <h3>How "robotic" is the bot?</h3>
                <p>It uses deterministic neural flows to ensure 100% accuracy based on your provided Q&A nodes.</p>
            </div>
            <div className="faq-item">
                <h3>Can I export the script?</h3>
                <p>Yes, any website can embed the FAQSense widget with a single line of code.</p>
            </div>
        </div>
    </section>
);

const Footer = () => (
    <footer className="footer">
        <div className="footer-content">
            <div className="footer-brand">
                <h3>FAQSense.ai</h3>
                <p>Your robot-first support partner.</p>
            </div>
            <div className="footer-bottom">
                &copy; 2026 FAQSense Inc. All rights reserved.
            </div>
        </div>
    </footer>
);

const LandingPage = () => {
    return (
        <div className="landing-page-container">
            <Navbar />
            <Hero />
            <Reviews />
            <FAQ />
            <Footer />
        </div>
    );
};

export default LandingPage;
