import React, { Component } from 'react';
import { Field , reduxForm } from 'redux-form';
import { Link } from 'react-router-dom'; 
import { connect } from 'react-redux';
import { createPost } from '../actions/index';


class PostsNew extends Component {

    renderField(field){
        const { meta : { touched , error } } = field; //Destructuring

        const className = `form-group ${touched && error ?  'has-danger' : ''}`

        return(
            <div className={className} > 
                <label>{field.label}</label>
                <input 
                    className="form-control"
                    type="text"
                    {...field.input} //This is an object which contains diff event handlers and props like onchange value of input and all properies which will be communicated to input tag      
                />
                <div className="text-help">
                {touched ? error : ''}
                </div>
            </div>
        )
    }


    onSubmit(values){
        this.props.createPost(values , () => {
            this.props.history.push('/'); // Will automatically redirect
        });
        
        console.log(values);
    }

    render(){
        const { handleSubmit } = this.props;
        return (
            <form onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                <Field 
                label="Title"
                name="title"
                component={this.renderField} //just an reference
                />
                <Field 
                label="Categories"
                name="categories" // this binds the validation
                component={this.renderField} //just an reference
                />
                <Field 
                label="Post Content"
                name="content"
                component={this.renderField} //just an reference
                />
                <button type="submit" className="btn btn-primary">
                Submit
                </button>
                <Link to="/" className="btn btn-danger">Cancel</Link>
            </form>
        );
    }
}

function validate(values){

    const errors = {}

    if(!values.title){
        errors.title = "Enter a title!"
    } 

    if(!values.categories){
        errors.categories = "Enter some categories!"
    } 

    if(!values.content){
        errors.content = "Enter some content please!"
    } 

    return errors; // Empty object means no error
}


export default reduxForm({
    validate,
    form:'PostsNewForm' //This string has to be unique
})(
    connect(null , {createPost})(PostsNew)
);