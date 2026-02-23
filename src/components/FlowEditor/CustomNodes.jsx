import React from 'react';
import { Handle, Position } from 'reactflow';

export const QuestionNode = ({ data }) => {
    return (
        <div style={{
            background: '#fff',
            border: '2px solid #6366f1',
            borderRadius: '12px',
            padding: '12px',
            minWidth: '200px',
            boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
            position: 'relative'
        }}>
            <div style={{ fontSize: '10px', fontWeight: 'bold', color: '#6366f1', marginBottom: '8px', textTransform: 'uppercase' }}>Question</div>
            <textarea
                value={data.label}
                onChange={(evt) => data.onChange(evt.target.value)}
                placeholder="Type question here..."
                style={{
                    width: '100%',
                    border: 'none',
                    resize: 'none',
                    outline: 'none',
                    fontSize: '14px',
                    color: '#1f2937',
                    background: 'transparent'
                }}
                rows={3}
            />
            <Handle type="source" position={Position.Right} style={{ background: '#6366f1' }} />
        </div>
    );
};

export const AnswerNode = ({ data }) => {
    return (
        <div style={{
            background: '#fff',
            border: '2px solid #10b981',
            borderRadius: '12px',
            padding: '12px',
            minWidth: '200px',
            boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
            position: 'relative'
        }}>
            <Handle type="target" position={Position.Left} style={{ background: '#10b981' }} />
            <div style={{ fontSize: '10px', fontWeight: 'bold', color: '#10b981', marginBottom: '8px', textTransform: 'uppercase' }}>Answer</div>
            <textarea
                value={data.label}
                onChange={(evt) => data.onChange(evt.target.value)}
                placeholder="Type answer here..."
                style={{
                    width: '100%',
                    border: 'none',
                    resize: 'none',
                    outline: 'none',
                    fontSize: '14px',
                    color: '#1f2937',
                    background: 'transparent'
                }}
                rows={3}
            />
        </div>
    );
};
