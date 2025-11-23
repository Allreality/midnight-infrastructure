// scavengerDropBatch.ts
// Node 18+, run with: NODE_OPTIONS="--max-old-space-size=2048" node --loader ts-node/esm scavengerDropBatch.ts

import fs from 'fs';
import readline from 'readline';
import { Lucid, Blockfrost, fromText } from 'lucid-cardano';
import 'dotenv/config';

const BF_PROJECT = process.env.BLOCKFROST_PROJECT!;
const NETWORK = 'Mainnet'; // or 'Preview' / 'Testnet'
const BATCH_SIZE = Number(process.env.BATCH_SIZE || 10);
const RECIPIENTS_FILE = './recipients.csv'; // simple CSV: address,lovelace

async function initLucid() {
  const lucid = await Lucid.new(new Blockfrost('https://cardano-mainnet.blockfrost.io/api/v0', BF_PROJECT), NETWORK);
  // Prefer injecting a signing key or use wallet adapter. Example: private key injection
  lucid.selectWalletFromPrivateKey(process.env.PRIVATE_KEY!);
  return lucid;
}

async function processBatches() {
  const lucid = await initLucid();

  const rl = readline.createInterface({
    input: fs.createReadStream(RECIPIENTS_FILE),
    crlfDelay: Infinity
  });

  let batch: { address: string; amount: bigint }[] = [];
  let lineCount = 0;

  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const [address, amountStr] = trimmed.split(',').map(s => s.trim());
    batch.push({ address, amount: BigInt(amountStr) });
    lineCount++;

    if (batch.length >= BATCH_SIZE) {
      await submitBatch(lucid, batch, Math.ceil(lineCount / BATCH_SIZE));
      batch = [];
      global.gc?.(); // if Node launched with --expose-gc
    }
  }

  if (batch.length > 0) {
    await submitBatch(lucid, batch, Math.ceil(lineCount / BATCH_SIZE));
    batch = [];
    global.gc?.();
  }

  console.log(`Done. Processed ${lineCount} recipients.`);
}

async function submitBatch(lucid: Lucid, batch: { address: string; amount: bigint }[], batchNumber: number) {
  console.log(`Submitting batch ${batchNumber} with ${batch.length} recipients...`);
  const tx = lucid.newTx();

  for (const { address, amount } of batch) {
    tx.payToAddress(address, { lovelace: amount });
  }

  const built = await tx.complete();
  const signed = await built.sign().complete();
  const txHash = await signed.submit();
  console.log(`Batch ${batchNumber} submitted: ${txHash}`);

  // Explicitly null references to help GC
  // @ts-ignore
  built.__proto__ = null;
  // @ts-ignore
  signed.__proto__ = null;
  await wait(500); // small pause to avoid spiking mem or API rate limits
}

function wait(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

processBatches().catch(err => {
  console.error('Fatal error', err);
  process.exit(1);
});