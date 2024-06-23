import styled from "styled-components";
import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { ago } from '../backend/util';
import * as allIcons from "tabler-icons-react";


const StyledVerticalBorder = styled.div`
  align-items: flex-start;
  background-color: #000000;
  border-color: #1C1C1E;
  border-right-style: solid;
  border-right-width: 1px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 16px 0.56px 0px 0px;
  position: relative;
  width: 450px;
  user-select: none;

  & .container {
    align-items: center;
    align-self: stretch;
    display: flex;
    flex: 1;
    flex-direction: column;
    flex-grow: 1;
    gap: 16px;
    padding: 24px 20px;
    position: relative;
    width: 100%;
  }

  & .frame-wrapper {
    align-items: flex-start;
    align-self: stretch;
    display: flex;
    flex: 0 0 auto;
    flex-direction: column;
    gap: 12px;
    padding: 0px 0px 12.01px;
    position: relative;
    width: 100%;
  }

  & .div {
    align-items: flex-start;
    display: inline-flex;
    flex: 0 0 auto;
    flex-direction: column;
    position: relative;
  }

  & .text-wrapper {
    color: #FFFFFF;
    font-family: "SF Pro Text-Semibold", Helvetica;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0;
    line-height: 28px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
    width: fit-content;
  }

  & .heading {
    align-items: flex-start;
    display: inline-flex;
    flex: 0 0 auto;
    flex-direction: column;
    margin-top: -2px;
    position: relative;
  }

  & .p {
    color: #A1A1AA;
    font-family: "SF Pro Text-Regular", Helvetica;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0;
    line-height: 24px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
    width: fit-content;
  }

  & .frame {
    align-items: flex-start;
    align-self: stretch;
    display: flex;
    flex: 0 0 auto;
    gap: 10px;
    position: relative;
    width: 100%;
  }

  & .text-wrapper-2 {
    color: #ffffff;
    font-family: "SF Pro Text-Bold", Helvetica;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0;
    line-height: 20px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
    width: fit-content;
  }

  & .nav {
    align-items: flex-start;
    align-self: stretch;
    display: flex;
    flex: 1;
    flex-direction: column;
    flex-grow: 1;
    gap: 4px;
    position: relative;
    width: 100%;
  }

  & .linkbruh {
    align-items: center;
    align-self: stretch;
    background-color: #ffffff0d;
    border-radius: 8px;
    display: flex;
    flex: 0 0 auto;
    padding: 8px;
    padding-left: 12px;
    position: relative;
    width: 100%;
    transition: background-color 0.3s ease; // Add smooth hover animation
    cursor: pointer;
}

& .linkbruh:hover {
    background-color: #ffffff1a; // Make the background slightly brighter on hover
}

  & .frame-2 {
    align-items: center;
    display: flex;
    flex: 1;
    flex-grow: 1;
    justify-content: space-between;
    position: relative;
  }

  & .frame-3 {
    align-items: center;
    display: inline-flex;
    flex: 0 0 auto;
    gap: 8px;
    height: 23.99px;
    position: relative;
  }

  & .img {
    flex: 0 0 auto;
    position: relative;
  }

  & .text-wrapper-3 {
    color: #ffffff;
    font-family: "SF Pro Text-Regular", Helvetica;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0;
    line-height: 20px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
    width: fit-content;
  }

  & .group {
    height: 23.99px;
    position: relative;
    width: 55px;
  }

  & .container-wrapper {
    align-items: center;
    display: inline-flex;
    position: relative;
  }

  & .overlay-wrapper {
    align-items: center;
    display: inline-flex;
    flex: 0 0 auto;
    gap: 7.99px;
    position: relative;
  }

  & .overlay {
    align-items: center;
    background-color: #22c55e1a;
    border-radius: 9999px;
    display: inline-flex;
    flex: 0 0 auto;
    height: 23.99px;
    padding: 3.99px 10px 4px 4px;
    position: relative;
  }

  & .background-wrapper {
    align-items: center;
    display: flex;
    height: 16px;
    justify-content: center;
    padding: 5px;
    position: relative;
    width: 16px;
  }

  & .background {
    background-color: #22c55e;
    border-radius: 9999px;
    height: 6px;
    position: relative;
    width: 6px;
    animation: blinkBackground 1s infinite; // Add blinking animation
  }

  @keyframes blinkBackground {
    0% {
        background-color: #22c55e;
    }
    50% {
        background-color: transparent;
    }
    100% {
        background-color: #22c55e;
    }
}

  & .margin {
    align-items: flex-start;
    display: inline-flex;
    flex: 0 0 auto;
    flex-direction: column;
    padding: 0px 0px 0px 2px;
    position: relative;
  }

  & .text-wrapper-4 {
    color: #22c55e;
    font-family: "SF Pro Text-Regular", Helvetica;
    font-size: 12px;
    font-weight: 400;
    letter-spacing: 0;
    line-height: 16px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
    width: fit-content;
  }

  & .text-wrapper-5 {
    color: #A1A1A1;
    font-family: "SF Pro Text-Regular", Helvetica;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0;
    line-height: 24px;
    position: relative;
    text-align: center;
    white-space: nowrap;
  }
`;


const HoverModal = styled.div`
  position: fixed;
  background-color: black;
  color: white;
  padding: 15px;
  border-radius: 5px;
  z-index: 1000;
  pointer-events: none;
  transition: opacity 0.2s ease-in-out;
  max-width: 300px;
  max-height: 400px;
  overflow-y: auto;
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
`;

export const Sidebar = ({ handleMouseEnter, handleMouseLeave, handleCallClick }) => {
    const calls = useSelector(state => state.calls);
    const [expandedCall, setExpandedCall] = useState(null);
  
    const toggleExpand = (callId) => {
      setExpandedCall(expandedCall === callId ? null : callId);
    };
  
    const sortedCalls = [...calls].sort((a, b) => b.createdDate - a.createdDate);
  
    return (
      <StyledVerticalBorder>
        <div className="container">
          <div className="frame-wrapper">
            <div className="div">
              <div className="div">
                <p className="text-wrapper">Call +1 (571) 651 8232</p>
              </div>
              <div className="heading">
                <p className="p">To experience the future of 911 calls.</p>
              </div>
            </div>
          </div>
          <div className="frame">
            <div className="text-wrapper-2">Recent Emergency Calls</div>
          </div>
          <div className="nav">
          {sortedCalls.map((call) => {
            const IconToBeUsed = allIcons[call.icon] || allIcons['Activity'];

            return (
              <div 
                className="linkbruh" 
                key={call.id} 
                onClick={() => {
                  toggleExpand(call.id);
                  handleCallClick(call);
                }}
                onMouseEnter={(e) => handleMouseEnter(e, call)}
                onMouseLeave={handleMouseLeave}
              >
                  <div className="frame-2">
                    <div className="frame-3">
                      <IconToBeUsed size={26} color="#ffffff" fill="#000000"  />
                      <div className="div">
                        <div className="text-wrapper-3">
                          {call.shortSummary ? call.shortSummary : ""}
                        </div>
                      </div>
                    </div>
                    {call.callStatus === "active" && (
                      <div className="group">
                        <div className="container-wrapper">
                          <div className="overlay-wrapper">
                            <div className="overlay">
                              <div className="background-wrapper">
                                <div className="background" />
                              </div>
                              <div className="margin">
                                <div className="text-wrapper-4">Live</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
          <div style={{ gap: "-2px", display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div className="text-wrapper-5">
        {"Built by "}
        <a href="https://twitter.com/cjarrayadev" style={{ textDecoration: "underline" }}>Christopher Arraya</a>
        {"  "}
        <a href="https://x.com/tahaha_a" style={{ textDecoration: "underline" }}>Taha Ansari</a>
        {""}
      </div>
      <div className="text-wrapper-5">
        <a href="https://x.com/JackBlair87" style={{ textDecoration: "underline" }}>Jack Blair</a>
        {"  "}
        <a href="https://twitter.com/rzhang139" style={{ textDecoration: "underline" }}>Richard Zhang</a>
      </div>
    </div>
        </div>
      </StyledVerticalBorder>
    );
  };