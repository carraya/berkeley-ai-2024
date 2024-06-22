// reducers.js
const initialState = {
  userData: [],
  userClassesData: [],
  selectedClassIndex: 0,
  selectedClassModerators: [],
  selectedClassResources: [],
  selectedClassUserChatsData: [],
  selectedChatContent: [],
  selectedChatID: "",
  selectedAIScholar: "pete",
};

const userReducer = (state = initialState, action) => {
  switch (action.type) {
    case "SET_USER_DATA":
      return {
        ...state,
        userData: action.payload,
      };
    case "SET_USER_CLASSES_DATA":
      return {
        ...state,
        userClassesData: action.payload,
      };
    case "SET_SELECTED_CLASS_INDEX":
      return {
        ...state,
        selectedClassIndex: action.payload,
      };
    case "SET_SELECTED_CLASS_MODERATORS":
      return { ...state, selectedClassModerators: action.payload };
    case "SET_SELECTED_CLASS_RESOURCES":
      return { ...state, selectedClassResources: action.payload };
    case "SET_SELCETED_CLASS_USER_CHATS_DATA":
      return { ...state, selectedClassUserChatsData: action.payload };
    case "SET_SELECTED_CHAT_CONTENT":
      return { ...state, selectedChatContent: action.payload };
    case "SET_SELECTED_CHAT_ID":
      return { ...state, selectedChatID: action.payload };
    case "SET_SELECTED_AI_SCHOLAR":
      return { ...state, selectedAIScholar: action.payload };
    case "APPEND_TO_LAST_MESSAGE": // Add this case
      const updatedChatContent = state.selectedChatContent.slice(); // Clone the array
      const lastMessageIndex = updatedChatContent.length - 1;
      const lastMessage = { ...updatedChatContent[lastMessageIndex] }; // Clone the last message
      lastMessage.content += action.payload;

      const newChatContent = [
        ...updatedChatContent.slice(0, lastMessageIndex),
        lastMessage,
        ...updatedChatContent.slice(lastMessageIndex + 1),
      ];

      return {
        ...state,
        selectedChatContent: newChatContent,
      };
      case "APPEND_RESOURCES_TO_LAST_MESSAGE":
        const updatedChatContent2 = [...state.selectedChatContent]; // Clone the array
        const lastMessageIndex2 = updatedChatContent2.length - 1;
        const lastMessage2 = { ...updatedChatContent2[lastMessageIndex2] }; // Clone the last message
        console.log("action.payload", action.payload);
      
        // Check if lastMessage2.resources is an array; if not, initialize it as an empty array
        if (!Array.isArray(lastMessage2.resources)) {
          lastMessage2.resources = [];
        }
      
        // Append the action.payload array to lastMessage2.resources
        lastMessage2.resources = [...lastMessage2.resources, ...action.payload];
      
        const newChatContent2 = [
          ...updatedChatContent2.slice(0, lastMessageIndex2),
          lastMessage2,
          ...updatedChatContent2.slice(lastMessageIndex2 + 1),
        ];
      
        return {
          ...state,
          selectedChatContent: newChatContent2,
        };
      
      
    default:
      return state;
  }
};

export default userReducer;
