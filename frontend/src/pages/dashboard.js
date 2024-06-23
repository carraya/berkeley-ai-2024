import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { ago } from '../backend/util';
import { setupCallsListener } from '../backend/subscriptions';
import { Sidebar } from '../components/Sidebar';
import Map from '../components/Map';
// import { Button } from '@/components/ui/button';

const Dashboard = () => {
  return (
    <div className="flex">
      <Sidebar />
      <Map />
    </div>
  );
};

export default Dashboard;