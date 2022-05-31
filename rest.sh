#!/bin/bash
systemctl daemon-reload
systemctl enable bot
systemctl start bot
systemctl status bot
