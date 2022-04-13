#!/bin/sh
npm update
cat package.json
npm install
npm run dev -- --host
