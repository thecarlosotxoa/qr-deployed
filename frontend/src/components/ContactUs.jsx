import React from "react";

const ContactUs = () => {
  return (
    <div className="p-8 bg-[#181818] text-slate-300 min-h-screen">
      <h1 className="text-3xl font-bold mb-4 text-slate-100">Contact Us</h1>
      <p className="mb-4">
        We value your feedback and are here to assist with any questions or
        concerns. Feel free to reach out to us at the following email address
      </p>
      <p>
        Email:{" "}
        <a
          href="mailto:tusolucionenlanube@gmail.com"
          className="text-blue-400 hover:underline"
        >
          tusolucionenlanube@gmail.com
        </a>
      </p>
    </div>
  );
};

export default ContactUs;
