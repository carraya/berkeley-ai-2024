import React, { useEffect } from 'react';
import { Sidebar } from '../components/Sidebar';
import Map from '../components/Map';
import { setupCallsListener } from '../backend/subscriptions';
// import { Button } from '@/components/ui/button';

const Dashboard = () => {

    useEffect(() => {
        const unsubscribe = setupCallsListener();
        return () => {
          unsubscribe();
        };
      }, []);

  return (
    <div className="flex">
      <Sidebar />
      <Map />
    </div>
  );
};

export default Dashboard;