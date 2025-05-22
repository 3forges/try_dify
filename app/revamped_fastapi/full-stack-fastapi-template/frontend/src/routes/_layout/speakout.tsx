import { useState } from "react";
import Controller from "./../../components/Speechtotext/Controller";
// import React from "react";
import * as React from "react"
import { createFileRoute, useNavigate } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/settings")({
  component: Speakout,
})

function Speakout() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <>
        <Controller />
      </>
    </div>
  );
}

export default Speakout;
