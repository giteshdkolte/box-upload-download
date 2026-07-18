## Setup

1. Create a Box Developer account by visiting:
   https://app.box.com/developers/console

2. Click **New App** and create a **Server Authentication (JWT)** application.

   <img src="./images/1.png" alt="Create Box App" width="1000">

3. Configure the application:
   - Select **JWT** as the authentication method.
   - Generate a **Public/Private Keypair** (this downloads the configuration file).
   - Copy the **Service Account (App User) email address** for later use.

   <img src="./images/2.0.png" alt="JWT authentication, Generate Keypair, and Service Account Email" width="1000">

   <img src="./images/2.1.png" alt="Downloaded Configuration File" width="500">

4. Open your Box account:
   https://app.box.com/

   Navigate to the folder you want to access and click **Share**.

   <img src="./images/3.0.png" alt="Share Folder" width="1000">

5. Invite the **Service Account (App User)** using the email copied in Step 3.
   - Grant the user **Editor** permission.
   - Accept the invitation if prompted.

   <img src="./images/3.1.png" alt="Grant Editor Access to Service Account" width="1000">

   <img src="./images/3.2.png" alt="Invitation Confirmation" width="500">

6. You're all set! You can now use the application to upload and download files from Box.

7. 🎉 Enjoy!