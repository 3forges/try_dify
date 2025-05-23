import { useState } from "react";
import Title from "./Title";
import axios from "redaxios";
import RecordMessage from "./RecordMessage";
// import React from "react";
import * as React from "react"


// CHAKRA SURGERY
import {
  Button,
  Flex,
  Heading,
  HStack,
  Input,
  Stack,
  Text,
} from '@chakra-ui/react';
import { Alert } from "@chakra-ui/react"
import { Spinner } from "@chakra-ui/react"

type MessageProps = {
  text: string;
  actor: 'user' | 'bot';
};
const Message = ({ text, actor }: MessageProps) => {
  return (
    <Flex
      p={4}
      bg={actor === 'user' ? 'blue.500' : 'gray.100'}
      color={actor === 'user' ? 'white' : 'gray.600'}
      borderRadius="lg"
      w="fit-content"
      alignSelf={actor === 'user' ? 'flex-end' : 'flex-start'}
    >
      <Text>{text}</Text>
    </Flex>
  );
};









const Controller = (): React.JSX.Element => {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  /*
  function createBlobURL(data: any) {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  }
  */

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // Append recorded message to messages
    const myMessage = { sender: "me", blobUrl };
    const messagesArr = [...messages, myMessage];

    // convert blob url to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // Construct audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        // send form data to api endpoint
        await axios
          .post("http://mongo.pesto.io:8000/api/v1/transcribe/", formData, {
            headers: {
              "Content-Type": "audio/mpeg",
            },
            // responseType: "arrayBuffer", // Set the response type to handle binary data
            responseType: "json",
          })
          .then((res: any) => {
            const transcribedMessage = res.data;
            // const audio = new Audio();
            // audio.src = createBlobURL(blob);

            // Append to audio
            const rachelMessage = { sender: "rachel", transcribedMessage: transcribedMessage };
            messagesArr.push(rachelMessage);
            setMessages(messagesArr);

            // Play audio
            setIsLoading(false);
            // audio.play();
          })
          .catch((err: any) => {
            console.error(err);
            setIsLoading(false);
          });
      });
  };

  return (
    <Flex h="100vh" py={12}>
      <Flex
        flexDirection="column"
        w="2xl"
        m="auto"
        h="full"
        borderWidth="1px"
        roundedTop="lg"
      >
        <HStack p={4} bg="blue.500">
          <Heading size="lg" color="white">
            Chat App
          </Heading>
        </HStack>

        <Stack
          px={4}
          py={8}
          overflow="auto"
          flex={1}
          css={{
            '&::-webkit-scrollbar': {
              width: '4px',
            },
            '&::-webkit-scrollbar-track': {
              width: '6px',
            },
            '&::-webkit-scrollbar-thumb': {
              background: '#d5e3f7',
              borderRadius: '24px',
            },
          }}
        >
          {messages?.map((message, index) => {
            return (
              <Message key={index + message.sender} text={message.transcribedMessage} actor={message.sender} />
            );
          })}

          {messages.length == 0 && !isLoading && (
            <Alert.Root status="info" title="This is the alert title">
              <Alert.Indicator />
              <Alert.Title>Send Rachel a message...</Alert.Title>
            </Alert.Root>
          )}

          {isLoading && (
          <Alert.Root status="info" title="This is the alert title">
            <Alert.Indicator />
            <Alert.Title> Gimme a few seconds...</Alert.Title>
            <Spinner size="sm" />
          </Alert.Root>
            

          )}
          <Message text="Hi" actor="user" />
          <Message text="How may I help you?" actor="bot" />
          <Message text="Hi" actor="user" />
          <Message text="How may I help you?" actor="bot" />
          <Message text="Hi" actor="user" />
          <Message text="How may I help you?" actor="bot" />
          <Message text="Hi" actor="user" />
          <Message text="How may I help you?" actor="bot" />
        </Stack>

        <HStack p={4} bg="gray.100">
          <Input bg="white" placeholder="Enter your text" />
          {/* Recorder */}
          <RecordMessage handleStop={handleStop} />
        </HStack>
      </Flex>
    </Flex>
  );
}
// END OF CHAKRA SURGERY

const ControllerOld = (): React.JSX.Element => {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  /*
  function createBlobURL(data: any) {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  }
  */

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // Append recorded message to messages
    const myMessage = { sender: "me", blobUrl };
    const messagesArr = [...messages, myMessage];

    // convert blob url to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // Construct audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        // send form data to api endpoint
        await axios
          .post("http://mongo.pesto.io:8000/api/v1/transcribe/", formData, {
            headers: {
              "Content-Type": "audio/mpeg",
            },
            // responseType: "arrayBuffer", // Set the response type to handle binary data
            responseType: "json",
          })
          .then((res: any) => {
            const transcribedMessage = res.data;
            // const audio = new Audio();
            // audio.src = createBlobURL(blob);

            // Append to audio
            const rachelMessage = { sender: "rachel", transcribedMessage: transcribedMessage };
            messagesArr.push(rachelMessage);
            setMessages(messagesArr);

            // Play audio
            setIsLoading(false);
            // audio.play();
          })
          .catch((err: any) => {
            console.error(err);
            setIsLoading(false);
          });
      });
  };

  return (
    <div className="h-screen overflow-y-hidden">
      {/* Title */}
      <Title setMessages={setMessages} />

      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        {/* Conversation */}
        <div className="mt-5 px-5">
          {messages?.map((message, index) => {
            return (
              <div
                key={index + message.sender}
                className={
                  "flex flex-col " +
                  (message.sender == "rachel" && "flex items-end")
                }
              >
                {/* Sender */}
                <div className="mt-4 ">
                  <p
                    className={
                      message.sender == "rachel"
                        ? "text-right mr-2 italic text-green-500"
                        : "ml-2 italic text-blue-500"
                    }
                  >
                    {message.sender}
                  </p>

                  {/* Message */}
                  {/**
                   *                   
                   * <audio
                   * src={audio.blobUrl}
                   * className="appearance-none"
                   * controls
                   * />
                   */}
                  <p
                    className={
                      message.sender == "rachel"
                        ? "text-right mr-2 italic text-green-500"
                        : "ml-2 italic text-blue-500"
                    }
                  >
                    {message.transcribedMessage}
                  </p>
                </div>
              </div>
            );
          })}

          {messages.length == 0 && !isLoading && (
            <div className="text-center font-light italic mt-10">
              Send Rachel a message...
            </div>
          )}

          {isLoading && (
            <div className="text-center font-light italic mt-10 animate-pulse">
              Gimme a few seconds...
            </div>
          )}
        </div>

        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <div>
              <RecordMessage handleStop={handleStop} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Controller;
