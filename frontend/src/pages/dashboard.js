import React, { useEffect, useState } from 'react';
import { Sidebar } from '../components/Sidebar';
import Map from '../components/Map';
import { setupCallsListener } from '../backend/subscriptions';
import styled from "styled-components";

const HoverModal = styled.div`
  position: fixed;
  background-color: black;
  color: white;
  padding: 15px;
  border-radius: 5px;
  z-index: 1000;
  pointer-events: none;
  transition: opacity 0.2s ease-in-out;
  max-width: 500px; /* Increased max-width */
  max-height: 600px; /* Increased max-height */
  overflow-y: auto;
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
`;

const Dashboard = () => {
  const [hoverInfo, setHoverInfo] = useState(null);

  const handleMouseEnter = (e, call) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setHoverInfo({
      call: call,
      x: rect.left + window.scrollX + rect.width / 2,
      y: rect.top + window.scrollY - 40,
    });
  };

  const handleMouseLeave = () => {
    setHoverInfo(null);
  };

  useEffect(() => {
    const unsubscribe = setupCallsListener();
    return () => {
      unsubscribe();
    };
  }, []);

  return (
    <div className="flex">
      <Sidebar
        handleMouseEnter={handleMouseEnter}
        handleMouseLeave={handleMouseLeave}
      />
      <Map />
      {hoverInfo && (
        <HoverModal>
          <div>
            <p>Call Status: {hoverInfo.call.callStatus}</p>
            <p>Created Date: {hoverInfo.call.createdDate}</p>
            <p>Icon: {hoverInfo.call.icon}</p>
            <p>Remaining JSON:</p>
            <pre>{JSON.stringify(hoverInfo.call, null, 2)}</pre>
          </div>
        </HoverModal>
      )}
    </div>
  );
};

export default Dashboard;
