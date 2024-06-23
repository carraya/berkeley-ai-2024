// import firebase from 'firebase/compat/app';
import app from '../firebase';
import 'firebase/compat/firestore';
import store from '../redux/store';
import { setCalls } from '../redux/actions';

export const setupCallsListener = () => {
  const firestore = app.firestore();
  const callsRef = firestore.collection('calls');

  return callsRef.onSnapshot((snapshot) => {
    const calls = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    store.dispatch(setCalls(calls));
  }, (error) => {
    console.error("Error in calls listener:", error);
  });
};