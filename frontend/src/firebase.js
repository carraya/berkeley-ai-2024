// see: https://firebase.google.com/docs/web/setup

// import firebase from "firebase/app"
// import "firebase/auth"
// import "firebase/firestore"
// import "firebase/analytics";

import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

import { GA4React } from "ga-4-react";

import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAQAJdypvRJpJUGMyg3EVvMAIX7Y5YwF-M",
  authDomain: "berkeley2024-d8b6a.firebaseapp.com",
  projectId: "berkeley2024-d8b6a",
  storageBucket: "berkeley2024-d8b6a.appspot.com",
  messagingSenderId: "990268880383",
  appId: "1:990268880383:web:3fdc5c0c7da782c51fa3ca",
  measurementId: "G-6Q7S9Y9SKW"
};


// const firebaseConfig = {
//     apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
//     authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
//     databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
//     projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
//     storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
//     messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
//     appId: process.env.REACT_APP_FIREBASE_APP_ID,
//     measurementId: "G-40CT6X3FQ0"
// }

//
// FIREBASE AUTH APP CONFIG
//
// https://firebase.google.com/docs/web/setup
// https://firebase.google.com/docs/reference/js/firebase
// https://firebase.google.com/docs/reference/js/firebase.auth

const app = firebase.initializeApp(firebaseConfig)
const analytics = getAnalytics(app);

export default app
