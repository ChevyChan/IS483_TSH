import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css"
import {
    MainContainer,
    ChatContainer,
    MessageList,
    Message,
    MessageInput,
    Avatar,
    Conversation,
    ConversationList,
    VoiceCallButton,
    VideoCallButton,
    TypingIndicator,
    Sidebar,
    Search,
    ConversationHeader,
    InfoButton,
    MessageSeparator,
} from "@chatscope/chat-ui-kit-react";

import {
    akaneModel,
    eliotModel,
    emilyModel,
    joeModel,
    lillyModel,
    kaiModel,
    zoeModel
} from '../data/AvatarData';

import React, { useEffect, useState } from "react";

function Chat(){
        // Set initial message input value to empty string                                                                     
        const [messageInputValue, setMessageInputValue] = useState("");
        return <div style={{
            height: "600px",
            width: "1200px",
            position: "relative"}}>
              <MainContainer responsive>                                   
                <Sidebar position="left" scrollable={true}>
                  <Search placeholder="Search..." />
                  <ConversationList>                                                     
                    <Conversation name="Lilly" lastSenderName="Lilly" info="Yes i can do it for you">
                      <Avatar src={lillyModel.avatar} name="Lilly" status="available" />
                    </Conversation>
                    
                    <Conversation name="Joe" lastSenderName="Joe" info="Yes i can do it for you">
                      <Avatar src={joeModel.avatar} name="Joe" status="dnd" />
                    </Conversation>
                    
                    <Conversation name="Emily" lastSenderName="Emily" info="Yes i can do it for you" unreadCnt={3}>
                      <Avatar src={emilyModel.avatar} name="Emily" status="available" />
                    </Conversation>
                    
                    <Conversation name="Kai" lastSenderName="Kai" info="Yes i can do it for you" unreadDot>
                      <Avatar src={kaiModel.avatar} name="Kai" status="unavailable" />
                    </Conversation>
                                
                    <Conversation name="Akane" lastSenderName="Akane" info="Yes i can do it for you">
                      <Avatar src={akaneModel.avatar} name="Akane" status="eager" />
                    </Conversation>
                                        
                    <Conversation name="Eliot" lastSenderName="Eliot" info="Yes i can do it for you">
                      <Avatar src={eliotModel.avatar} name="Eliot" status="away" />
                    </Conversation>
                                                        
                    <Conversation name="Zoe" lastSenderName="Zoe" info="Yes i can do it for you" active>
                      <Avatar src={zoeModel.avatar} name="Zoe" status="dnd" />
                    </Conversation>
                    
                    <Conversation name="Patrik" lastSenderName="Patrik" info="Yes i can do it for you">
                      <Avatar src={kaiModel.avatar} name="Patrik" status="invisible" />
                    </Conversation>
                                                                             
                  </ConversationList>
                </Sidebar>
                  
                <ChatContainer>
                  <ConversationHeader>
                    <ConversationHeader.Back />
                    <Avatar src={zoeModel.avatar} name="Zoe" />
                    <ConversationHeader.Content userName="Zoe" info="Active 10 mins ago" />
                    <ConversationHeader.Actions>
                      <VoiceCallButton />
                      <VideoCallButton />
                      <InfoButton />
                    </ConversationHeader.Actions>          
                  </ConversationHeader>
                  <MessageList typingIndicator={<TypingIndicator content="Zoe is typing" />}>
                    
                    <MessageSeparator content="Saturday, 30 November 2019" />
                    
                    <Message model={{
                    message: "Hello my friend",
                    sentTime: "15 mins ago",
                    sender: "Zoe",
                    direction: "incoming",
                    position: "single"
                    }}>
                      <Avatar src={zoeModel.avatar} name="Zoe" />
                    </Message>
                    
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Patrik",
                        direction: "outgoing",
                        position: "single"
                    }} avatarSpacer />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Zoe",
                        direction: "incoming",
                        position: "first"
                    }} avatarSpacer />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Zoe",
                        direction: "incoming",
                        position: "normal"
                    }} avatarSpacer />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Zoe",
                        direction: "incoming",
                        position: "normal"
                    }} avatarSpacer />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Zoe",
                        direction: "incoming",
                        position: "last"
                    }}>
                      <Avatar src={zoeModel.avatar} name="Zoe" />
                    </Message>
                    
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Patrik",
                        direction: "outgoing",
                        position: "first"
                    }} />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Patrik",
                        direction: "outgoing",
                        position: "normal"
                    }} />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Patrik",
                        direction: "outgoing",
                        position: "normal"
                    }} />
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Patrik",
                        direction: "outgoing",
                        position: "last"
                    }} />
                    
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Zoe",
                        direction: "incoming",
                        position: "first"
                    }} avatarSpacer />                                          
                    <Message model={{
                        message: "Hello my friend",
                        sentTime: "15 mins ago",
                        sender: "Zoe",
                        direction: "incoming",
                        position: "last"
                    }}>
                      <Avatar src={zoeModel.avatar} name="Zoe" />
                    </Message>
                  </MessageList>
                  <MessageInput placeholder="Type message here" value={messageInputValue} onChange={val => setMessageInputValue(val)} onSend={() => setMessageInputValue("")} />
                </ChatContainer>
              </MainContainer>
            </div>;
    
}

export default Chat;
