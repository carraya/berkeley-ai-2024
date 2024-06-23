// import firebase from 'firebase/compat/app';
import app from '../firebase';
import 'firebase/compat/firestore';
import store from '../redux/store';
import { setCalls } from '../redux/actions';

export const setupCallsListener = () => {
  const firestore = app.firestore();
  const callsRef = firestore.collection('calls').orderBy('createdDate', 'desc').limit(10);

  return callsRef.onSnapshot((snapshot) => {
    console.log("Calls listener triggered");
    const calls = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    console.log("Calls:", calls);
    store.dispatch(setCalls(calls));
  }, (error) => {
    console.error("Error in calls listener:", error);
  });
};