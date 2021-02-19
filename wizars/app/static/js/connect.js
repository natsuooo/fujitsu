const Peer = window.Peer;

(async function main() {
    let localStream;
    const myVideo = document.getElementById('my-video');
    const myID = document.getElementById('my-id');
    const remoteVideo = document.getElementById('remote-video');
    const remoteID = document.getElementById('remote-id');
    const makeCall = document.getElementById('make-call');
    const closeCall = document.getElementById('make-close');


    // カメラ映像取得
    navigator.mediaDevices.getUserMedia({video: true, audio: true})
        .then( stream => {
        // 成功時にvideo要素にカメラ映像をセットし、再生
        myVideo.srcObject = stream;
        myVideo.play();
        // 着信時に相手にカメラ映像を返せるように、グローバル変数に保存しておく
        localStream = stream;
    }).catch( error => {
        // 失敗時にはエラーログを出力
        console.error('mediaDevice.getUserMedia() error:', error);
        return;
    });

    //Peer作成
    const peer = (window.peer = new Peer({
        key: window.__SKYWAY_KEY__
      }));
    peer.on('open', () => {
        myID.textContent = peer.id;
    });

    //呼び出し処理
    makeCall.addEventListener('click',() =>{
      if (!peer.open) {
        return;
      }
      const mediaConnection = peer.call(remoteID.value, localStream);
      mediaConnection.on('stream', async stream => {
        remoteVideo.srcObject = stream;
        remoteVideo.playsInline = true;
        await remoteVideo.play().catch(console.error);
      });
  
      mediaConnection.once('close', () => {
        remoteVideo.srcObject.getTracks().forEach(track => track.stop());
        remoteVideo.srcObject = null;
      });

      //切断処理
      closeCall.addEventListener('click', () => mediaConnection.close(true));
    });
  
  // イベントリスナを設置する関数
  const setEventListener = mediaConnection => {
    mediaConnection.on('stream', stream => {
      // video要素にカメラ映像をセットして再生
      remoteVideo.srcObject = stream;
      remoteVideo.play();
    });
  }
  //着信処理
  peer.on('call', mediaConnection => {
    mediaConnection.answer(localStream);
    setEventListener(mediaConnection);
    mediaConnection.once('close',() =>{
      remoteVideo.srcObject.getTracks().forEach(track => track.stop());
      remoteVideo.srcObject = null;
    });
    //切断処理
    closeCall.addEventListener('click', () => mediaConnection.close(true));
  });
  
  peer.on('error', console.error);
})();
//参照(https://github.com/skyway/skyway-js-sdk)//