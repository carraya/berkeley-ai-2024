// actions.js
export const SET_USER_DATA = 'SET_USER_DATA';
export const SET_USER_CLASSES_DATA = 'SET_USER_CLASSES_DATA';

export const SET_SELECTED_CLASS_INDEX = 'SET_SELECTED_CLASS_INDEX';
export const SET_SELECTED_CLASS_MODERATORS = 'SET_SELECTED_CLASS_MODERATORS';
export const SET_SELECTED_CLASS_RESOURCES = 'SET_SELECTED_CLASS_RESOURCES';

export const SET_SELECTED_CHAT_CONTENT = 'SET_SELECTED_CHAT_CONTENT';
export const SET_SELECTED_CHAT_ID = 'SET_SELECTED_CHAT_ID';

export const SET_SELECTED_AI_SCHOLAR = 'SET_SELECTED_AI_SCHOLAR';

export const SET_SELCETED_CLASS_USER_CHATS_DATA = 'SET_SELCETED_CLASS_USER_CHATS_DATA';

export const APPEND_TO_LAST_MESSAGE = 'APPEND_TO_LAST_MESSAGE';
export const APPEND_RESOURCES_TO_LAST_MESSAGE = 'APPEND_RESOURCES_TO_LAST_MESSAGE';

export const setUserData = (userData) => ({
  type: SET_USER_DATA,
  payload: userData,
});

export const setUserClassesData = (userClassesData) => ({
  type: SET_USER_CLASSES_DATA,
  payload: userClassesData,
});

export const setSelectedClassIndex = (selectedClassIndex) => ({
  type: SET_SELECTED_CLASS_INDEX,
  payload: selectedClassIndex,
});

export const setSelectedClassModerators = (selectedClassModerators) => ({
  type: SET_SELECTED_CLASS_MODERATORS,
  payload: selectedClassModerators,
});

export const setSelectedClassResources = (selectedClassResources) => ({
  type: SET_SELECTED_CLASS_RESOURCES,
  payload: selectedClassResources,
});

export const setSelectedChatContent = (selectedChatContent) => ({
  type: SET_SELECTED_CHAT_CONTENT,
  payload: selectedChatContent,
});

export const setSelectedChatId = (selectedChatId) => ({
  type: SET_SELECTED_CHAT_ID,
  payload: selectedChatId,
});

export const setSelectedAIScholar = (selectedAIScholar) => ({
  type: SET_SELECTED_AI_SCHOLAR,
  payload: selectedAIScholar,
});

export const setSelectedClassUserChatsData = (selectedClassUserChatsData) => ({
  type: SET_SELCETED_CLASS_USER_CHATS_DATA,
  payload: selectedClassUserChatsData,
});

export const appendToLastMessage = (chunk) => ({
  type: APPEND_TO_LAST_MESSAGE,
  payload: chunk,
});

export const appendResourcesToLastMessage = (resources) => ({
  type: APPEND_RESOURCES_TO_LAST_MESSAGE,
  payload: resources,
});


// Define an action creator to update the selected class index, moderators, and other relevant state items
export const setSelectedStateAndModerators = (
  selectedClassIndex,
  selectedClassModerators,
  selectedClassResources,
  selectedClassUserChatsData,
  selectedChatContent,
  selectedChatID,
  selectedAIScholar
) => (dispatch) => {
  dispatch(setSelectedClassIndex(selectedClassIndex));
  dispatch(setSelectedClassModerators(selectedClassModerators));
  dispatch(setSelectedClassResources(selectedClassResources));
  dispatch(setSelectedClassUserChatsData(selectedClassUserChatsData));
  dispatch(setSelectedChatContent(selectedChatContent));
  dispatch(setSelectedChatId(selectedChatID));
  dispatch(setSelectedAIScholar(selectedAIScholar));

  // Save the data to localStorage
  const stateToSave = {
    selectedClassIndex,
    selectedClassModerators,
    selectedClassResources,
    selectedClassUserChatsData,
    selectedChatContent,
    selectedChatID,
    selectedAIScholar,
  };
  localStorage.setItem('userState', JSON.stringify(stateToSave));
};
