import { combineReducers } from 'redux';
import PostsReducer from './reducer_post'
import { reducer as formReducer } from 'redux-form';

// here keyword form is mandatory
const rootReducer = combineReducers({
  posts:PostsReducer,
  form: formReducer
});

export default rootReducer;
