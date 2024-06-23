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
  transition: opacity 0.2s ease-in-out;
  max-width: 500px;
  max-height: 600px;
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
  const [selectedCall, setSelectedCall] = useState(null);

  const handleMouseEnter = (e, call) => {
    if (!selectedCall) {
      const rect = e.currentTarget.getBoundingClientRect();
      setHoverInfo({
        call: call,
        x: rect.left + window.scrollX + rect.width / 2,
        y: rect.top + window.scrollY - 40,
      });
    }
  };

  const handleMouseLeave = () => {
    if (!selectedCall) {
      setHoverInfo(null);
    }
  };

  const handleCallClick = (call) => {
    setSelectedCall(call);
    setHoverInfo({
      call: call,
      x: window.innerWidth / 2,
      y: window.innerHeight / 2,
    });
  };

  const handleModalClose = () => {
    setSelectedCall(null);
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
        handleCallClick={handleCallClick}
      />
      <Map />
      {(hoverInfo || selectedCall) && (
        <HoverModal onClick={selectedCall ? handleModalClose : undefined} style={{ cursor: selectedCall ? 'pointer' : 'default' }}>
          <div>
            <p>Call Status: {(selectedCall || hoverInfo.call).callStatus}</p>
            <p>Created Date: {(selectedCall || hoverInfo.call).createdDate}</p>
            <p>Icon: {(selectedCall || hoverInfo.call).icon}</p>
            <p>Remaining JSON:</p>
            <pre>{JSON.stringify(selectedCall || hoverInfo.call, null, 2)}</pre>
            {selectedCall && <p>Click anywhere on this modal to close</p>}
          </div>
        </HoverModal>
      )}
    </div>
  );
};

export default Dashboard;