import React, { useState, useCallback } from 'react';
import ReactFlow, {
    addEdge,
    Background,
    Controls,
    applyEdgeChanges,
    applyNodeChanges
} from 'reactflow';
import 'reactflow/dist/style.css';
import './FlowEditor.css';

const initialNodes = [
    {
        id: '1',
        data: { label: 'Q: How to reset password?' },
        position: { x: 250, y: 5 },
        type: 'input'
    },
    {
        id: '2',
        data: { label: 'A: Go to settings and click reset.' },
        position: { x: 250, y: 100 }
    },
];

const initialEdges = [{ id: 'e1-2', source: '1', target: '2' }];

const FlowEditor = () => {
    const [nodes, setNodes] = useState(initialNodes);
    const [edges, setEdges] = useState(initialEdges);

    const onNodesChange = useCallback(
        (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [setNodes]
    );
    const onEdgesChange = useCallback(
        (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [setEdges]
    );
    const onConnect = useCallback(
        (connection) => setEdges((eds) => addEdge(connection, eds)),
        [setEdges]
    );

    const handleSave = () => {
        const flowData = { nodes, edges };
        console.log('Saving flow data:', flowData);
        alert('Flow saved to console! (Backend integration pending)');
    };

    const addNode = () => {
        const newNode = {
            id: (nodes.length + 1).toString(),
            data: { label: `New Node ${nodes.length + 1}` },
            position: { x: Math.random() * 400, y: Math.random() * 400 },
        };
        setNodes((nds) => nds.concat(newNode));
    };

    const handleDownloadTemplate = () => {
        const csvContent = "Questions,Answers\n" +
            "Hi,Hello! How can I help you today?\n" +
            "Hello,Greetings! What can 1 assist you with?\n" +
            "What is FAQSense?,FAQSense is an AI-powered FAQ management and chatbot platform.\n";

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", "faq_template.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="flow-editor-wrapper">
            <div className="flow-toolbar">
                <button onClick={addNode}>Add Node</button>
                <button className="template-btn" onClick={handleDownloadTemplate}>Download FAQ Template</button>
                <div className="upload-container">
                    <button className="upload-btn">Upload FAQs</button>
                    <div className="info-tooltip">
                        <span className="tooltip-icon">?</span>
                        <div className="tooltip-content">Supports CSV and Excel files</div>
                    </div>
                </div>
                <button className="save-btn" onClick={handleSave}>Save Flow</button>
            </div>
            <div className="flow-container">
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    fitView
                >
                    <Background />
                    <Controls />
                </ReactFlow>
            </div>
        </div>
    );
};

export default FlowEditor;
