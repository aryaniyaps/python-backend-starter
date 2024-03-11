import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { MAX_EMAIL_LENGTH } from '@/lib/constants';
import useAuthenticateStart from '@/lib/hooks/useAuthenticateStart';
import { zodResolver } from '@hookform/resolvers/zod';
import { DialogClose } from '@radix-ui/react-dialog';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

const changeEmailSchema = z.object({
  newEmail: z
    .string()
    .min(1, { message: 'Email address is required' })
    .email({ message: 'Email address is invalid' })
    .max(MAX_EMAIL_LENGTH),
});

export default function ChangeEmailDialog() {
  const form = useForm({
    resolver: zodResolver(changeEmailSchema),
    defaultValues: { newEmail: '' },
  });

  const authenticateStart = useAuthenticateStart();

  async function onSubmit(values: z.infer<typeof changeEmailSchema>) {
    try {
      // start webauthn authentication
      // FIXME: we need an API method to re authenticate without requiring email
      const data = await authenticateStart.mutateAsync({ email: '' });
    } catch (err) {
      // TODO: handle errors better
    }
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button size='icon'>
          <Icons.penBox className='h-6 w-6' />
        </Button>
      </DialogTrigger>

      <DialogContent className='sm:max-w-[425px]'>
        <DialogHeader>
          <DialogTitle>Change email address</DialogTitle>
          <DialogDescription>
            We'll send a verification code to your new email address
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex w-full flex-col gap-6'
          >
            <FormField
              control={form.control}
              name='newEmail'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>New email address</FormLabel>
                  <FormControl>
                    <Input placeholder='new@example.com' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <DialogFooter className='flex w-full items-end gap-4'>
              <DialogClose asChild>
                <Button variant='ghost'>Cancel</Button>
              </DialogClose>
              <Button type='submit'>Send verification code</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
