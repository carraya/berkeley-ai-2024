// import { configureStore } from '@reduxjs/toolkit';
// import rootReducer from './reducers';

// // Load saved state from localStorage
// const savedState = localStorage.getItem('userState');
// const preloadedState = savedState ? JSON.parse(savedState) : undefined; // Set preloadedState to undefined when there is no saved state

// const store = configureStore(savedState ? {
//   reducer: rootReducer,
//   preloadedState: preloadedState, // Pass the loaded state as preloadedState, which could be undefined
// } : {
//   reducer: rootReducer,
// });

// // Subscribe to store changes to save the state in localStorage
// store.subscribe(() => {
//   const currentState = store.getState();
//   const stateToSave = {
//     selectedClassIndex: currentState.selectedClassIndex,
//     selectedClassModerators: currentState.selectedClassModerators,
//     selectedClassResources: currentState.selectedClassResources,
//     selectedClassUserChatsData: currentState.selectedClassUserChatsData,
//     selectedChatContent: currentState.selectedChatContent,
//     selectedChatID: currentState.selectedChatID,
//     selectedAIScholar: currentState.selectedAIScholar,
//   };
//   // console.log("Saving state to localStorage:", stateToSave);
//   localStorage.setItem('userState', JSON.stringify(stateToSave));
// });

// export default store;



import { configureStore } from '@reduxjs/toolkit';
import callsReducer from './reducers';

const store = configureStore({
  reducer: callsReducer,
});

export default store;

