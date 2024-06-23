import { SET_CALLS } from "./actions";

const initialState = {
  calls: [],
};

const callsReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_CALLS:
      return {
        ...state,
        calls: action.payload,
      };
    default:
      return state;  }
};

export default callsReducer;