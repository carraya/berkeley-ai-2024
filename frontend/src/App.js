import ReactGA from "react-ga";
import { Provider } from "react-redux";
import React from "react";
import store from "./redux/store";
import Dashboard from "./pages/dashboard";
import Map from "./pages/Map";

const GA_TRACKER_ID = process.env.REACT_APP_GA_TRACKER_ID;
const GA_DEBUG_MODE = process.env.REACT_APP_GA_DEBUG_MODE === "true";
ReactGA.initialize(GA_TRACKER_ID, { debug: GA_DEBUG_MODE });

function App() {
  ReactGA.pageview(window.location.href);

  // Debug mode setup
  var DEBUG = window.location.href.indexOf("localhost") > -1;
  if(!DEBUG){
    if(!window.console) window.console = {};
    var methods = ["log", "debug", "warn", "info"];
    for(var i=0;i<methods.length;i++){
      console[methods[i]] = function(){};
    }
  }

  return (
    <Provider store={store}>
      <div className="app-container">
        <div className="dashboard-panel">
          <Dashboard />
        </div>
        <div className="map-container">
          <Map />
        </div>
      </div>
    </Provider>
  );
}

export default App;