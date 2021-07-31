import React, { Component, useEffect, useState, useRef, useImperativeHandle } from "react";
import axios from 'axios';


const DeleteComment = (c_id)=>{

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const url = window.location.protocol+'//'+window.location.host;


   return( fetch(`${url}/api/update_delete_comment/${c_id}/`, {
      method: 'DELETE',
      mode: 'same-origin',
      credentials: 'include',
      headers: {
        'content-type': 'multipart/form-data' ,
        'X-CSRFToken': csrftoken
      },

    }))
    }
const CommentFetch = (post_id) => {
    const url = window.location.protocol+'//'+window.location.host;
    return(fetch(url+`/api/get_comment/${post_id}`, {
      method: 'GET',
    }).then((response) => {
        if(response.status==200){
            const datas = response.json()
          return datas
        }else{
          console.log('error')
        }
        }))
}

const TimelinePostsFetch = (user_id, next) => {
let url;

if(next){
  url = next;
}else{
  url = window.location.protocol+'//'+window.location.host+`/api/timelinepost/${user_id}/`;
}


  return(fetch(url, {
    method: 'GET',
  }).then((response) => {
      if(response.ok){
        return response.json()
      }else{
        return false
      }
      }))
}


const TimelineProfileFetch = (user_id) => {
  let url;
  

    url = window.location.protocol+'//'+window.location.host+`/api/timelineprof/${user_id}/`;
  
  
  
    return(fetch(url, {
      method: 'GET',
    }).then((response) => {
        if(response.ok){
          return response.json()
        }else{
          return false
        }
        }))
  }

const PostShare = (formData, formmp)=>{
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;





    let header;

    let bodys;
  if(formmp){
    header={
      headers: {
        'X-CSRFToken': csrftoken
      }
    }
  
    bodys={
      body:formData
    }
  }else{
    let object = {}
    formData.forEach(function(value, key){
      key!=='image'?object[key] = value:null;
        
  
    });
    let json = JSON.stringify(object);
    
    bodys={
      body:json
    }
    header={
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      }
    }
  }






  const url = window.location.protocol+'//'+window.location.host;

    
    
    
    return (fetch(url+'/api/post/', {
      method: 'POST',
      mode: 'same-origin',
      credentials: 'include',
      ...header,
      ...bodys

    }).then((response) => {

      if (response.ok) {
        console.log(response)

        return response.json();
      } else {
        throw new Error('Something went wrong');
      }



    }))
}

const AcceptRequestFunc = (current)=>{
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const cdata = {
      "friend": current,
  };
  const url = window.location.protocol+'//'+window.location.host;

  return fetch(url+'/api/accept/', {
    method: 'POST',
    mode: 'same-origin',
    credentials: 'include',
    headers: {
    'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(cdata)

  }).then((response) => {
      if(response.status===201){
          console.log(response)

          
          return response.json()

      }
  })
}

const SendFriendRequestFunc = (current)=>{
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const cdata = {
      "friend_requests": current,
  };
  const url = window.location.protocol+'//'+window.location.host;

  return fetch(url+'/api/send_request/', {
    method: 'POST',
    mode: 'same-origin',
    credentials: 'include',
    headers: {
    'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(cdata)

  }).then((response) => {
      if(response.ok){
          return response.json()

      }else{
        return false
      }
  })
}

const LogoutFunc = ()=>{
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const url = window.location.protocol+'//'+window.location.host;

  return fetch(url+'/api/auth/logout/', {
    method: 'POST',
    mode: 'same-origin',
    credentials: 'include',
    headers: {
    'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({})

  }).then((response) => {
      if(response.ok){
          return response.json()

      }else{
        return false
      }
  })
}






const SearchMethod = (...args)=>{


    const url = window.location.protocol+'//'+window.location.host+'/api/search/';
    let name = '';
    if(args.length===1){
        name=args[0]
    }else if(args.length>1){
        name=args[0]+'-'+args[1]
    }


    return(fetch(url+name+'/', {
      method: 'GET',
    }).then((response) => {
        if(response.status==200){
            const datas = response.json()
          return datas
        }else{
          console.log('error')
        }
        }))
}
const GetFriends = () => {
  const url = window.location.protocol+'//'+window.location.host;
  return(fetch(url+`/api/friend_requests/`, {
    method: 'GET',
  }).then((response) => {
      if(response.status==200){
          const datas = response.json()
          console.log(datas)
        return datas
      }else{
        console.log('error')
      }
      }))
}




export {
    DeleteComment,
    CommentFetch,
    PostShare,
    SearchMethod,
    GetFriends,
    AcceptRequestFunc,
    TimelinePostsFetch,
    TimelineProfileFetch,
    SendFriendRequestFunc,
    LogoutFunc
};