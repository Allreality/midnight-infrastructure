// File: src/lib/midnight.ts
// Location: /mnt/c/projects/midnight-infrastructure/midnight-dapp/src/lib/midnight.ts

import { MidnightSetupAPI } from '@meshsdk/midnight-setup';

export const midnight = new MidnightSetupAPI({
  walletProvider: 'lace',
  network: 'preprod',
});