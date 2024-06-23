import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { ago } from '../backend/util';
import { setupCallsListener } from '../backend/subscriptions';
import { Sidebar } from '../components/Sidebar';
// import { Button } from '@/components/ui/button';

const Dashboard = () => {
  const calls = useSelector(state => state.calls);
  const [expandedCall, setExpandedCall] = useState(null);

  useEffect(() => {
    const unsubscribe = setupCallsListener();
    return () => {
      unsubscribe();
    };
  }, []);

  const toggleExpand = (callId) => {
    setExpandedCall(expandedCall === callId ? null : callId);
  };

  const sortedCalls = [...calls].sort((a, b) => b.createdDate - a.createdDate);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-grow p-4">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
        <p className="mb-4">Dashboard content goes here</p>
        <h2 className="text-xl font-semibold mb-2">Calls</h2>

        {sortedCalls.map(call => (
          <div key={call.id} className="mb-2">
            <button
              onClick={() => toggleExpand(call.id)}
              className="w-full text-left"
            >
              Call {call.id} - {ago(call.createdDate)}
            </button>
            {expandedCall === call.id && (
              <pre className="mt-2 p-2 bg-gray-100 rounded overflow-x-auto">
                {JSON.stringify(call, null, 2)}
              </pre>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;