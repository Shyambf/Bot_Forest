#!/bin/bash
systemctl daemon-reload
systemctl stop bot
systemctl start bot
systemctl status bot
