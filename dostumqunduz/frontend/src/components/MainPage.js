import React, { Component, useEffect, useState } from "react";
import AuthHome from './isauth/AuthHome';
import GuestHome from "./isguest/GuestHome";



export default function MainPage(props){


  const [profile, setProfile ] = useState({'name':null,
  'last_name':null,
  'picture':'',
  'gender':null,
  'id':null,
})
  const [isauth, setIsauth] = useState(false)
  const [fr_posts, setFr_posts] = useState([])
  const [next, setNext] = useState(null)



  const RedirectAuth = ()=>{
    window.location.reload()

    
  }

  useEffect(()=>{
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    const is_authenticated = document.getElementById('is_authenticated').textContent;
    if(is_authenticated=='True'){
      setIsauth(true)
      loadFriendsPosts()
    }else{
      setIsauth(false)

    }
  }, [])




  useEffect(()=>{
 
      loadScreen()

  }, [props])




  const loadScreen = ()=>{
    setProfile(props.CurrentUser)
  }

  const loadFriendsPosts = ()=>{
    const url = window.location.protocol+'//'+window.location.host;
        fetch(url+'/api/friends_posts/', {
          method: 'GET',
        }).then((response) => {
          if(response.ok){
            return response.json()
          }else{
            return {error:true, status:response.status}
          }
          
          }).then(data=>{ 
            if(!data.error){
              setFr_posts(data.results)
              setNext(data.next)

            }else{
              console.log(data.status)

            }
        })
    
      }






      const loadMoreFriendsPosts = (url)=>{
            return(fetch(url, {
              method: 'GET',
            }).then((response) => {
              if(response.ok){
                return response.json()
              }else{
                return false
              }
              
              }).then(data=>{ 
                setFr_posts([...fr_posts, ...data.results])
                setNext(data.next)
   


            }))
        
          }


    if(isauth){
      return (
        <AuthHome loadFriendsPosts={loadFriendsPosts} CurrentUserId={props.CurrentUser.id} next={next} loadMoreFriendsPosts={loadMoreFriendsPosts} fr_posts={fr_posts} profile={profile}/>
      );
    }else{
      return <GuestHome RedirectAuth={RedirectAuth}/>

    }

  
}