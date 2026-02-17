import React from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';

const AuthPage = ({ type }) => {
    return (
        <div className="auth-container">
            <div className="auth-card">
                <Link to="/" className="back-home">← Back to FAQSense</Link>
                <h2>{type === 'login' ? 'Welcome Back' : 'Join the Revolution'}</h2>
                <p>{type === 'login' ? 'Log in to your robotic dashboard' : 'Create your free developer account'}</p>

                <form className="auth-form" onSubmit={(e) => e.preventDefault()}>
                    {type === 'signup' && (
                        <div className="input-group">
                            <label>Full Name</label>
                            <input type="text" placeholder="John Doe" />
                        </div>
                    )}
                    <div className="input-group">
                        <label>Email Address</label>
                        <input type="email" placeholder="robot@faqsense.ai" />
                    </div>
                    <div className="input-group">
                        <label>Password</label>
                        <input type="password" placeholder="••••••••" />
                    </div>

                    <button type="submit" className="auth-btn">
                        {type === 'login' ? 'Login' : 'Sign Up'}
                    </button>
                </form>

                <div className="auth-footer">
                    {type === 'login' ? (
                        <span>Don't have an account? <Link to="/signup">Sign Up</Link></span>
                    ) : (
                        <span>Already have an account? <Link to="/login">Login</Link></span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AuthPage;
