'use client';

import { SlotProps } from 'input-otp';

export function OTPSlot(props: SlotProps) {
  return (
    <div
      className={
        'relative h-unit-14 w-unit-10 px-unit-4 py-unit-4 text-center text-2xl font-semibold ' +
        'flex items-center justify-center ' +
        'transition-all duration-300 ' +
        'border border-divider bg-background first:mr-unit-1 '
      }
    >
      {props.char !== null && <div>{props.char}</div>}
      {props.hasFakeCaret && <OTPCaret />}
    </div>
  );
}

// You can emulate a fake textbox caret!
function OTPCaret() {
  return (
    <div className='animate-caret-blink pointer-events-none absolute inset-0 flex items-center justify-center'>
      <div className='h-unit-8 w-px bg-white' />
    </div>
  );
}
