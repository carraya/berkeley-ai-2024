import React from "react";
import styled from "styled-components";

const StyledVerticalBorder = styled.div`
  align-items: flex-start;
  background-color: #000000;
  border-color: var(--dashboardmintlifycomnero-5);
  border-right-style: solid;
  border-right-width: 0.56px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 16px 0.56px 0px 0px;
  position: relative;
  width: 300px;
  user-select: none;
  height: 100vh;

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
    font-weight: 400;
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
    color: var(--dashboardmintlifycomnero-40);
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

  & .link {
    align-items: center;
    align-self: stretch;
    background-color: #ffffff0d;
    border-radius: 8px;
    display: flex;
    flex: 0 0 auto;
    padding: 8px;
    position: relative;
    width: 100%;
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
    color: #a1a1aa;
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
    color: var(--dashboardmintlifycomnero-40);
    font-family: "SF Pro Text-Regular", Helvetica;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0;
    line-height: 24px;
    position: relative;
    text-align: center;
    white-space: nowrap;
    width: fit-content;
  }
`;

export const Sidebar = () => {
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
          <div className="link">
            <div className="frame-2">
              <div className="frame-3">
                <img className="img" alt="Container" src="container.svg" />
                <div className="div">
                  <div className="text-wrapper-3">Robbery at Berkeley</div>
                </div>
              </div>
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
            </div>
          </div>
          <div className="link">
            <div className="frame-2">
              <div className="frame-3">
                <img className="img" alt="Container" src="image.svg" />
                <div className="div">
                  <div className="text-wrapper-3">Robbery at Berkeley</div>
                </div>
              </div>
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
            </div>
          </div>
          <div className="link">
            <div className="frame-2">
              <div className="frame-3">
                <img className="img" alt="Container" src="container-2.svg" />
                <div className="div">
                  <div className="text-wrapper-3">Robbery at Berkeley</div>
                </div>
              </div>
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
            </div>
          </div>
        </div>
        <div className="text-wrapper-5">Built by Yo Mama</div>
      </div>
    </StyledVerticalBorder>
  );
};
