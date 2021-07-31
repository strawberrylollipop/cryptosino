import React, { Component, useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";
import { icons } from "./Icons";

function PostFunc({post, key, children}){



return(
    <div key={key}>
    <div className="postProf">
    <div className="postProfPic m0">
        {post.userprof.picture?<img className="profImg" src={post.userprof.picture} />:post.userprof.gender?icons.guy_prof:icons.girl_prof}

        
        
        </div>
        <Link className="no-decoration" to={'/timeline/'+post.userprof.user}><div className="postProfName">{post.userprof.name} {post.userprof.last_name}</div></Link>
    </div>
    <div className="postBody">{post.body}</div>
    {(()=>{

if(post.image){
    return <div className="postDivImage"><img className="postImgImage w400" src={post.image} /></div>
}
})()}

{children}
</div>

    )
}

export {
    PostFunc
};