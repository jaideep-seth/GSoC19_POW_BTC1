import sys
import time
import libtorrent as lt

#Create torrent
fs = lt.file_storage()
lt.add_files(fs, input("\n File location"))
t = lt.create_torrent(fs)
trackerList = ['udp://tracker.coppersurfer.tk:6969',
           'udp://tracker.opentrackr.org:1337/announce',
           'udp://torrent.gresille.org:80/announce',
           'udp://9.rarbg.me:2710/announce',
           'udp://p4p.arenabg.com:1337',
           'udp://tracker.internetwarriors.net:1337']

for tracker in trackerList:        
  t.add_tracker(tracker, 0)
  t.set_creator('libtorrent %s' % lt.version)
  t.set_comment("Test")
  lt.set_piece_hashes(t, ".")
  torrent = t.generate()    
  f = open("mytorrent.torrent", "wb")
  f.write(lt.bencode(torrent))
  f.close()

  #Seed torrent
  ses = lt.session()
  ses.listen_on(6881, 6891)
  h = ses.add_torrent({'ti': lt.torrent_info('mytorrent.torrent'), 'save_path': '.', 'seed_mode': True}) 
  print("Total size: " + str(h.status().total_wanted))
  print("Name: " + h.name())   
  while h.is_seed():
      s = h.status()
      state_str = ['queued', 'checking', 'downloading metadata', \
        'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

      print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
        (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
      sys.stdout.flush()

      time.sleep(1)
