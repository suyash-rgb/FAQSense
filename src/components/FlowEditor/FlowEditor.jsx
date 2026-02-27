import React, { useState, useCallback, useEffect, useMemo } from 'react';
import ReactFlow, {
    addEdge,
    Background,
    Controls,
    applyEdgeChanges,
    applyNodeChanges,
    MiniMap,
    ReactFlowProvider,
    useReactFlow
} from 'reactflow';
import 'reactflow/dist/style.css';
import './FlowEditor.css';
import { QuestionNode, AnswerNode } from './CustomNodes';

const nodeTypes = {
    question: QuestionNode,
    answer: AnswerNode,
};

const FlowEditorContent = ({ initialData, onSave }) => {
    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);
    const [rfInstance, setRfInstance] = useState(null);
    const { fitView } = useReactFlow();

    const onNodeDataChange = useCallback((id, newLabel) => {
        setNodes((nds) =>
            nds.map((node) => {
                if (node.id === id) {
                    return {
                        ...node,
                        data: {
                            ...node.data,
                            label: newLabel,
                        },
                    };
                }
                return node;
            })
        );
    }, []);

    const createPair = useCallback((yIndex, qText = '', aText = '') => {
        const id = Math.random().toString(36).substring(2, 9);
        const qId = `q-${id}`;
        const aId = `a-${id}`;

        const qNode = {
            id: qId,
            type: 'question',
            data: {
                label: qText,
                onChange: (val) => onNodeDataChange(qId, val)
            },
            position: { x: 100, y: yIndex * 180 + 50 },
        };

        const aNode = {
            id: aId,
            type: 'answer',
            data: {
                label: aText,
                onChange: (val) => onNodeDataChange(aId, val)
            },
            position: { x: 500, y: yIndex * 180 + 50 },
        };

        const edge = {
            id: `e-${id}`,
            source: qId,
            target: aId,
            animated: true,
            style: { stroke: '#6366f1', strokeWidth: 2 }
        };

        return { nodes: [qNode, aNode], edges: [edge] };
    }, [onNodeDataChange]);

    useEffect(() => {
        if (initialData && initialData.length > 0) {
            let allNodes = [];
            let allEdges = [];
            initialData.forEach((item, index) => {
                const { nodes: pNodes, edges: pEdges } = createPair(
                    index,
                    item.Question || item.Questions || item.question || '',
                    item.Answer || item.Answers || item.answer || ''
                );
                allNodes = [...allNodes, ...pNodes];
                allEdges = [...allEdges, ...pEdges];
            });
            setNodes(allNodes);
            setEdges(allEdges);

            // Allow time for render before fitView
            setTimeout(() => fitView(), 100);
        } else if (nodes.length === 0) {
            // Start with one empty pair if totally empty
            const { nodes: pNodes, edges: pEdges } = createPair(0);
            setNodes(pNodes);
            setEdges(pEdges);
        }
    }, [initialData]);

    const onNodesChange = useCallback(
        (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [setNodes]
    );
    const onEdgesChange = useCallback(
        (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [setEdges]
    );
    const onConnect = useCallback(
        (connection) => {
            setEdges((eds) => {
                // Each question can only have ONE unique answer. 
                // If user connects it to another answer, we replace the previous edge.
                const filteredEdges = eds.filter(e => e.source !== connection.source);
                return addEdge(
                    { ...connection, animated: true, style: { stroke: '#6366f1', strokeWidth: 2 } },
                    filteredEdges
                );
            });
        },
        [setEdges]
    );

    const handleSave = () => {
        const csvRows = [];
        edges.forEach(edge => {
            const sourceNode = nodes.find(n => n.id === edge.source);
            const targetNode = nodes.find(n => n.id === edge.target);

            if (sourceNode && targetNode) {
                const question = sourceNode.data.label;
                const answer = targetNode.data.label;
                if (question || answer) {
                    csvRows.push({ Question: question, Answer: answer });
                }
            }
        });

        if (onSave) {
            onSave(csvRows);
        }
    };

    const addFAQPair = () => {
        const nextIndex = Math.floor(nodes.length / 2);
        const { nodes: pNodes, edges: pEdges } = createPair(nextIndex);
        setNodes((nds) => nds.concat(pNodes));
        setEdges((eds) => eds.concat(pEdges));

        // Slightly delay fitView to allow nodes to be added to DOM
        setTimeout(() => fitView({ duration: 800 }), 100);
    };

    const addNode = (type) => {
        const id = `${type.charAt(0)}-${Date.now()}`;
        const newNode = {
            id,
            type,
            data: {
                label: '',
                onChange: (val) => onNodeDataChange(id, val)
            },
            position: { x: Math.random() * 200 + 50, y: Math.random() * 200 + 50 },
        };
        setNodes((nds) => nds.concat(newNode));
    };

    return (
        <div className="flow-editor-wrapper">
            <div className="flow-toolbar">
                <div className="toolbar-left">
                    <button className="add-btn" onClick={addFAQPair}>
                        <span>+</span> Add FAQ Pair
                    </button>
                    <button className="add-node-btn question" onClick={() => addNode('question')}>
                        <span>+</span> Question
                    </button>
                    <button className="add-node-btn answer" onClick={() => addNode('answer')}>
                        <span>+</span> Answer
                    </button>
                    <div className="flow-stats">
                        {Math.floor(nodes.length / 2)} FAQ Pairs
                    </div>
                </div>
                <div className="toolbar-right">
                    <button className="clear-btn" onClick={() => { setNodes([]); setEdges([]); }}>Clear All</button>
                    <button className="save-btn" onClick={handleSave}>Apply & Save Changes</button>
                </div>
            </div>
            <div className="flow-container" style={{ height: '600px', width: '100%', background: '#fafbfc' }}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    nodeTypes={nodeTypes}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onInit={setRfInstance}
                    fitView
                    snapToGrid
                    snapGrid={[15, 15]}
                >
                    <Background color="#e2e8f0" gap={20} />
                    <Controls />
                    <MiniMap
                        nodeColor={(n) => n.type === 'question' ? '#6366f1' : '#10b981'}
                        maskColor="rgba(241, 245, 249, 0.6)"
                    />
                </ReactFlow>
            </div>
            <div className="flow-footer">
                <p>Drag nodes to organize. Double click text to edit. <strong>Rule:</strong> Each question maps to 1 answer, but an answer can have multiple paraphrased questions pointing to it.</p>
            </div>
        </div>
    );
};

const FlowEditor = (props) => (
    <ReactFlowProvider>
        <FlowEditorContent {...props} />
    </ReactFlowProvider>
);

export default FlowEditor;
