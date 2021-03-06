import React, { Component, useEffect, useState, useRef } from "react";
import { LoginFunc, RegisterFunc } from "./LoginRegisterFunctions";

export default function GuestHome (props){
  
const [state, setState] = useState({picture:''}) 
const [Form, SetForm] = useState('daxil_ol')
const [Email, SetEmail] = useState('')
const [Password, SetPassword] = useState('')
const [RePassword, SetRePassword] = useState('')
const [PassDontMatch, SetPassDontMatch] = useState(false)
const [ErrorInfo, SetErrorInfo] = useState(false)
const [RegError, SetRegError] = useState(false)
const [ErrorNetwork, SetErrorNetwork] = useState(false)
const [Name, SetName] = useState('')
const [LastName, SetLastName] = useState('')
const [Gender, SetGender] = useState('')
const [Picture, SetPicture] = useState(null)




      const toggle = {
        daxil_ol: 'qeydiyyat',
        qeydiyyat: 'daxil_ol'
      };





const OnLogin = (e)=>{
      e.preventDefault();

        LoginFunc(Email, Password).then((x)=>{
          if(x==='403'){
            
            props.RedirectAuth()
          }else if(!x){
            SetErrorInfo(true)
            SetErrorNetwork(false)
          }else{
            SetErrorInfo(false)
            SetErrorNetwork(false)


            props.RedirectAuth()
          }

      }).catch((err)=>{
        SetErrorInfo(false)
        SetErrorNetwork(true)

      })




  
    }
    const OnRegister = (e)=>{
        e.preventDefault();

        if(Password===RePassword){

            let cgender;
            Gender==='male'?cgender=true:cgender=false;
            const formData = new FormData()

            formData.append('email', Email)
            formData.append('password', Password)
            formData.append('name', Name)
            formData.append('last_name', LastName)
            formData.append('gender', cgender)
            formData.append('picture', Picture)



            RegisterFunc(formData, Picture).then((x)=>{
              if(!x){
                SetErrorInfo(false)
                SetErrorNetwork(false)
                SetPassDontMatch(false)
                SetRegError(true)
                console.log(x.status)

              }else{
                SetErrorInfo(false)
                SetErrorNetwork(false)
                SetRegError(false)
                SetPassDontMatch(false)

                props.RedirectAuth()
              }
            }).catch((err)=>{
              SetRegError(false)
              SetErrorInfo(false)
              SetPassDontMatch(false)
              SetErrorNetwork(true)

            })


        }else{
          SetPassDontMatch(true)
        }
      }

      const handleChange = (event) => {
        const tname = event.target['name']
        const tvalue = event.target.value


        if(tname==='uname'){
          SetName(tvalue)
        
        }else if(tname==='last_name'){
          SetLastName(tvalue)
        }else if(tname==='gender'){
          SetGender(tvalue)
        }else if(tname==='picture'){
          SetPicture(event.target.files[0])
        }else if(tname==='email'){
          SetEmail(tvalue)
        }else if(tname==='password'){
          SetPassword(tvalue)
        }else if(tname==='repassword'){
          SetRePassword(tvalue)
        }
           
            }





      return (
        <div className={"form-container "+Form}>
          <div style={{transform: `translate(${Form === 'daxil_ol' ? 0 : 290}px, 0px)`}} className="form-form-div">
            <form onSubmit={Form==='daxil_ol'?OnLogin:OnRegister}>
              {Form==='qeydiyyat'?(
              <>
              <input name="uname" placeholder="Ad" value={Name} onChange={handleChange} required />
              <input name="last_name" placeholder="Soyad" value={LastName} onChange={handleChange} required />
              
              <select className="ml5" name="gender" value={Gender} onChange={handleChange} required >
                <option value="" defaultChecked>Cinsinizi seçin</option>
                <option value="female">Qadın</option>
                <option value="male">Kişi</option>
              </select>
              <label className="w400 flex align-items-center ml10" htmlFor="picture">
                <div className="up-label">Profil şəkli seç (qeyri-məcburi):</div>

              <input className="w100p" name="picture" type='file' value={state.picture} onChange={handleChange} />
              </label>
        
              </>
              ):null}
              <input name="email" placeholder="Email" type="email" value={Email} onChange={handleChange} required />
              <input name="password" placeholder="Şifrə Yazın" type="password" value={Password} onChange={handleChange} required />
              {Form === 'daxil_ol' ? (<><button className="form-button-primary">Daxil ol</button>{ErrorInfo?<div className="red ml5">Email və ya parol yanlışdır</div>:ErrorNetwork?<div className="red">İnternet bağlantınızda problem yarandı</div>:''}</>): (
              <>
                <input name="repassword" placeholder="Şifrəni Təkrarlayın" type="password" value={RePassword} onChange={handleChange} required />
                {PassDontMatch?<div className="red ml10">Şifrələr üst-üstə düşmür</div>:RegError?<div className="red ml10">Bu email ilə artıq qeydiyyatdan keçilib</div>:ErrorNetwork?<div className="red ml10">Zəhmət olmasa internet bağlantınızı yoxlayın</div>:null}
                <button className="form-button-primary">Qeydiyyat</button>
              </>)}
              
              
            </form>
          </div>
          <div style={{transform: `translate(${Form === 'daxil_ol' ? 0 : -650}px, 0px)`}} className="form-button-div">
            <p>{Form === 'daxil_ol' ? 'Hesabınız yoxdur?' : 'Artıq üzvüsünüz?'}</p>
            <button onClick={() => {
              SetForm(toggle[Form])
              }}>{toggle[Form]}</button>
          </div>
        </div>
      );

  }



