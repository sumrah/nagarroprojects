import React, { Component } from 'react';
import { connect } from 'react-redux';
import { fetchPost , deletePost } from '../actions/index';
import { Link } from 'react-router-dom';

class PostsShow extends Component{
    componentDidMount(){
       // if(!this.props.post){  // Not fetching if already exists
        const { id } = this.props.match.params;
        console.log(id);
        this.props.fetchPost(id);
      //  }
    }

    onDeleteClick(){
        const { id } = this.props.match.params;
        this.props.deletePost(id , () =>{
            this.props.history.push('/');
        });
    }


     render(){
        const { post } = this.props;

        if(!post){
            return <div>Loading</div>;
        }

         /// posts[this.props.match.param.id] Get the particular post from whole posts object 
         return(
             <div>
                 <Link to ="/" className="btn btn-primary">Back To Index</Link>
                 <button
                 className = "btn btn-danger pull-xs-right"
                 onClick = {this.onDeleteClick.bind(this)}
                 >
                 Delete Post
                </button>
                 <h3>{post.title}</h3>
                 <h6>Categories: {post.categories} </h6>
                 <p>{post.content}</p>
             </div>    
         );
     }
}

function mapStateToProps({ posts } , ownProps ){
    return { post : posts[ownProps.match.params.id] };
}

export default connect(mapStateToProps , { fetchPost , deletePost })(PostsShow);
