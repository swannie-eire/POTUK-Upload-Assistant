from selenium.webdriver.support.ui import WebDriverWait
from urllib import request as urllib_request
import pickle
from selenium import webdriver
from time import sleep
import traceback
from src.console import console
import re
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher
import asyncio
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.trackers.COMMON import COMMON
import os
from torf import Torrent
from urllib.parse import urlencode, unquote
import xml.etree.ElementTree
from http.cookiejar import CookieJar
from pymediainfo import MediaInfo


class POTUK():

    def __init__(self, config):
        self.config = config
        self.source_flag = 'POTUK'
        self.username = config['TRACKERS']['POTUK'].get('username')
        self.password = config['TRACKERS']['POTUK'].get('password')
        self.headless = config['SELENIUM'].get('headless')
        self.tracker = 'POTUK'
        self.message = "################################################\n"
        self.cookie_path = config['SELENIUM'].get('cookie_path')
        self.gecko_driver = config['SELENIUM'].get('gecko_driver')
        # self.upload_url = 'https://beyond-hd.me/api/upload/'
        # self.forum_link = 'https://beyond-hd.me/rules'
        self.tv_types = ["sci-fi / supernatural / horror", "comedy", "crime / action / adventure", "drama", "documentary", "cartoons/animation", "sport tv", "misc tv", "generic"]
        self.tv_links = ["https://www.potuk.net/index.php?forums/sci-fi-supernatural-horror.68/post-thread", "https://www.potuk.net/index.php?forums/comedy.69/post-thread", "https://www.potuk.net/index.php?forums/action-adventure.72/post-thread", "https://www.potuk.net/index.php?forums/drama.71/post-thread", "https://www.potuk.net/index.php?forums/documentaries.75/post-thread", "https://www.potuk.net/index.php?forums/cartoons-animation.70/post-thread", "https://www.potuk.net/index.php?forums/sport-tv.66/post-thread", "https://www.potuk.net/index.php?forums/misc-tv.73/post-thread", "https://www.potuk.net/index.php?forums/tv-shows.64/post-thread"]

        self.movie_types = ["Cams TS & TC/PPV/VOD/HDTV", "Screeners/R3/R5/R6/HDRip/Webrip/WEB-DL/Recodes", "DVDRip/BRRip/BDRip", "DVDR", "High Definition MKV/MP4", "4k Ultra High Definition", "generic"]
        self.movie_links = ["https://www.potuk.net/index.php?forums/cams-ts-tc-ppv-vod-hdtv-ratio-free.16/post-thread", "https://www.potuk.net/index.php?forums/screeners-r3-r5-r6-hdrip-webrip-web-dl-recodes.10/post-thread", "https://www.potuk.net/index.php?forums/dvdrip-brrip-bdrip.9/post-thread", "https://www.potuk.net/index.php?forums/dvdr.11/post-thread", "https://www.potuk.net/index.php?forums/high-definition-mkv-mp4.15/post-thread", "https://www.potuk.net/index.php?forums/4k-ultra-high-definition-ratio-free.17/post-thread", "https://www.potuk.net/index.php?forums/movies.8/post-thread"]

        # used for test
        self.tv_links = ["https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                         "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",]

        #Used for testing should be uncommented
        self.movie_links = ["https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                            "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                            "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                            "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                            "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                            "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread",
                            "https://www.potuk.net/index.php?forums/practice-your-uploading-skills-in-here.132/post-thread"]

        pass

    def login(self, driver):

        user_entry = driver.find_element("name", "login")
        user_entry.clear()
        user_entry.send_keys(self.username)

        pass_entry = driver.find_element("name", "password")
        pass_entry.clear()
        # http://192.168.0.1/html/reboot.html
        pass_entry.send_keys(self.password)
        #driver.find_element_by_class_name("button--primary.button.button--icon.button--icon--login").click()
        # this is not working for some reason
        # delete cookie and it should work then
        #driver.find_element_by_class_name("button--primary.button.button--icon.button--icon--login").click()
        driver.find_element(By.CLASS_NAME, "button--primary.button.button--icon.button--icon--login").click()
        # below works but gives me an error using click instead
        #driver.find_element_by_class_name("button--primary.button.button--icon.button--icon--login").submit().send_keys(Keys.ENTER)
        #sleep(5)

    def get_movie_type(self, definition, source, is_disc, type, sd):
        # print("movie type = ", definition, source, is_disc, type, sd)
        # checking if episode
        if definition == "2160p" and not(type.lower().__contains__("hdrip") or type.lower().__contains__("web") or type.lower().__contains__("scr")):
            # print("movie type = 5 2160p", definition, source, is_disc, type, sd)
            return 5
        elif  sd and is_disc:
            # print("movie type = 3 disc ", definition, source, is_disc, type, sd)
            return 3
        elif type.lower().__contains__("hdrip") or type.lower().__contains__("hd-rip") or type.lower().__contains__("web") or type.lower().__contains__("scr") :
            # print("movie type = 1 web ", definition, source, is_disc, type, sd)
            return 1
        elif sd:
            # print("movie type = 2 sd ", definition, source, is_disc, type, sd)
            return 2
        elif definition == "1080p" or definition == "720p":
            # print("movie type = 4 1080 or 720 ", definition, source, is_disc, type, sd)
            return 4
        elif source.lower().__contains__("hdtv"):
            # print("movie type = 0 Cams ", definition, source, is_disc, type, sd)
            return 0
        else:
            return 6


    def get_series_type(self, movie):
        index = 7
        # tv is catergorised via genre so need to find genre and use that to determine section to upload in.
        genres = movie['genres'].split()
        if any("Sci-Fi" in s for s in genres) or any("Horror" in s for s in genres) or any("Fantasy" in s for s in genres):
            return 0
        elif any("Drama" in s for s in genres):
            return 3

        for i in genres:
            g = i.lower().replace(',', '')
            for s in self.tv_types:
                if s.__contains__(g):
                    return self.tv_types.index(s)

        return index


    def check_if_contains(self, driver, word):
        if word in driver.page_source:
            return True
        else:
            return False


    def identify_type(self, t_name, movie):
        definition = ""
        source = ""
        #use to id if film/movie etc..
        # use to id if single episode or multiple eps etc..
        type = movie['media_type']

        if re.search('1080', t_name, re.IGNORECASE):
            definition = "1080p"
        elif re.search('720', t_name, re.IGNORECASE):
            definition = "720p"
        elif re.search('4k', t_name, re.IGNORECASE):
            definition = "2160p"
        elif re.search('2160', t_name, re.IGNORECASE):
            definition = "2160p"
        elif re.search('UHD', t_name, re.IGNORECASE):
            definition = "2160p"
        else:
            definition = "SD"
        if re.search('HDTV', t_name, re.IGNORECASE):
            source = "HDTV"
        elif re.search('hdrip', t_name, re.IGNORECASE) or re.search('hd-rip', t_name, re.IGNORECASE)  or re.search('web', t_name, re.IGNORECASE) or re.search('scr', t_name, re.IGNORECASE):
            source = "hdrip"
        elif re.search('WEB', t_name, re.IGNORECASE):
            source = "WEB"
        elif re.search('Bluray', t_name, re.IGNORECASE) or re.search('BRRIP', t_name, re.IGNORECASE) or re.search('BDRIP', t_name, re.IGNORECASE):
            source = "BRRIP"
        elif re.search('DVDrip', t_name, re.IGNORECASE):
            source = "DVDrip"
        elif re.search("dvdr", t_name, re.IGNORECASE) or re.search("dvd-r", t_name, re.IGNORECASE):
            source = "DVD-r"
        else:
            source = "none"

        # if ufc in title or boxing in title put in sports section.
        # If boxing a keyword and contains vs in title or has sport as another keyword put in sport section
        if "ufc" in movie['title'].lower() or "boxing" in movie['title'].lower() or ("boxing" in movie['keywords'].lower() and ("vs" in movie['title'].lower()) and ("sport" in movie['keywords'].lower() or "sports" in movie['keywords'].lower()) ):
            #cprint('It is Sport', 'grey', 'on_yellow')
            console.print(f"[yellow]It is Sport")
            return 6
        elif type.lower().__contains__("movie"):
            return self.get_movie_type(movie['resolution'], movie['source'], movie['is_disc'], movie['type'], movie['sd'])
        elif type.lower().__contains__("series") or type.lower().__contains__("episode") or type.lower().__contains__("tv"):
            return self.get_series_type(movie)
        else:
            print("Error!!! POT unable to find type for {0} {1}".format(t_name,type))
            exit(8)


    def click_checkbox(self, checkbox):
        if not checkbox.is_selected():
            checkbox.send_keys(Keys.SPACE)


    def checked_if_url_changed(self, driver, field):
        try:
            delay = 5  # seconds
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, field)))
            return True
        except:
            return False


    async def upload(self, meta):
        common = COMMON(config=self.config)
        await self.edit_desc(meta, self.tracker)
        description = open(f"{meta['base_dir']}/tmp/{meta['uuid']}/[{self.tracker}]DESCRIPTION.txt", 'r').read()


        url = "https://www.potuk.net/"
        options = Options()
        options.headless = self.headless

        download_location = f"{meta['base_dir']}/tmp/{meta['uuid']}/"
        #
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference('browser.download.dir', download_location)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.hzn-3d-crossword,video/3gpp,video/3gpp2,application/vnd.mseq,application/vnd.3m.post-it-notes,application/vnd.3gpp.pic-bw-large,application/vnd.3gpp.pic-bw-small,application/vnd.3gpp.pic-bw-var,application/vnd.3gp2.tcap,application/x-7z-compressed,application/x-abiword,application/x-ace-compressed,application/vnd.americandynamics.acc,application/vnd.acucobol,application/vnd.acucorp,audio/adpcm,application/x-authorware-bin,application/x-athorware-map,application/x-authorware-seg,application/vnd.adobe.air-application-installer-package+zip,application/x-shockwave-flash,application/vnd.adobe.fxp,application/pdf,application/vnd.cups-ppd,application/x-director,applicaion/vnd.adobe.xdp+xml,application/vnd.adobe.xfdf,audio/x-aac,application/vnd.ahead.space,application/vnd.airzip.filesecure.azf,application/vnd.airzip.filesecure.azs,application/vnd.amazon.ebook,application/vnd.amiga.ami,applicatin/andrew-inset,application/vnd.android.package-archive,application/vnd.anser-web-certificate-issue-initiation,application/vnd.anser-web-funds-transfer-initiation,application/vnd.antix.game-component,application/vnd.apple.installe+xml,application/applixware,application/vnd.hhe.lesson-player,application/vnd.aristanetworks.swi,text/x-asm,application/atomcat+xml,application/atomsvc+xml,application/atom+xml,application/pkix-attr-cert,audio/x-aiff,video/x-msvieo,application/vnd.audiograph,image/vnd.dxf,model/vnd.dwf,text/plain-bas,application/x-bcpio,application/octet-stream,image/bmp,application/x-bittorrent,application/vnd.rim.cod,application/vnd.blueice.multipass,application/vnd.bm,application/x-sh,image/prs.btif,application/vnd.businessobjects,application/x-bzip,application/x-bzip2,application/x-csh,text/x-c,application/vnd.chemdraw+xml,text/css,chemical/x-cdx,chemical/x-cml,chemical/x-csml,application/vn.contact.cmsg,application/vnd.claymore,application/vnd.clonk.c4group,image/vnd.dvb.subtitle,application/cdmi-capability,application/cdmi-container,application/cdmi-domain,application/cdmi-object,application/cdmi-queue,applicationvnd.cluetrust.cartomobile-config,application/vnd.cluetrust.cartomobile-config-pkg,image/x-cmu-raster,model/vnd.collada+xml,text/csv,application/mac-compactpro,application/vnd.wap.wmlc,image/cgm,x-conference/x-cooltalk,image/x-cmx,application/vnd.xara,application/vnd.cosmocaller,application/x-cpio,application/vnd.crick.clicker,application/vnd.crick.clicker.keyboard,application/vnd.crick.clicker.palette,application/vnd.crick.clicker.template,application/vn.crick.clicker.wordbank,application/vnd.criticaltools.wbs+xml,application/vnd.rig.cryptonote,chemical/x-cif,chemical/x-cmdf,application/cu-seeme,application/prs.cww,text/vnd.curl,text/vnd.curl.dcurl,text/vnd.curl.mcurl,text/vnd.crl.scurl,application/vnd.curl.car,application/vnd.curl.pcurl,application/vnd.yellowriver-custom-menu,application/dssc+der,application/dssc+xml,application/x-debian-package,audio/vnd.dece.audio,image/vnd.dece.graphic,video/vnd.dec.hd,video/vnd.dece.mobile,video/vnd.uvvu.mp4,video/vnd.dece.pd,video/vnd.dece.sd,video/vnd.dece.video,application/x-dvi,application/vnd.fdsn.seed,application/x-dtbook+xml,application/x-dtbresource+xml,application/vnd.dvb.ait,applcation/vnd.dvb.service,audio/vnd.digital-winds,image/vnd.djvu,application/xml-dtd,application/vnd.dolby.mlp,application/x-doom,application/vnd.dpgraph,audio/vnd.dra,application/vnd.dreamfactory,audio/vnd.dts,audio/vnd.dts.hd,imag/vnd.dwg,application/vnd.dynageo,application/ecmascript,application/vnd.ecowin.chart,image/vnd.fujixerox.edmics-mmr,image/vnd.fujixerox.edmics-rlc,application/exi,application/vnd.proteus.magazine,application/epub+zip,message/rfc82,application/vnd.enliven,application/vnd.is-xpr,image/vnd.xiff,application/vnd.xfdl,application/emma+xml,application/vnd.ezpix-album,application/vnd.ezpix-package,image/vnd.fst,video/vnd.fvt,image/vnd.fastbidsheet,application/vn.denovo.fcselayout-link,video/x-f4v,video/x-flv,image/vnd.fpx,image/vnd.net-fpx,text/vnd.fmi.flexstor,video/x-fli,application/vnd.fluxtime.clip,application/vnd.fdf,text/x-fortran,application/vnd.mif,application/vnd.framemaker,imae/x-freehand,application/vnd.fsc.weblaunch,application/vnd.frogans.fnc,application/vnd.frogans.ltf,application/vnd.fujixerox.ddd,application/vnd.fujixerox.docuworks,application/vnd.fujixerox.docuworks.binder,application/vnd.fujitu.oasys,application/vnd.fujitsu.oasys2,application/vnd.fujitsu.oasys3,application/vnd.fujitsu.oasysgp,application/vnd.fujitsu.oasysprs,application/x-futuresplash,application/vnd.fuzzysheet,image/g3fax,application/vnd.gmx,model/vn.gtw,application/vnd.genomatix.tuxedo,application/vnd.geogebra.file,application/vnd.geogebra.tool,model/vnd.gdl,application/vnd.geometry-explorer,application/vnd.geonext,application/vnd.geoplan,application/vnd.geospace,applicatio/x-font-ghostscript,application/x-font-bdf,application/x-gtar,application/x-texinfo,application/x-gnumeric,application/vnd.google-earth.kml+xml,application/vnd.google-earth.kmz,application/vnd.grafeq,image/gif,text/vnd.graphviz,aplication/vnd.groove-account,application/vnd.groove-help,application/vnd.groove-identity-message,application/vnd.groove-injector,application/vnd.groove-tool-message,application/vnd.groove-tool-template,application/vnd.groove-vcar,video/h261,video/h263,video/h264,application/vnd.hp-hpid,application/vnd.hp-hps,application/x-hdf,audio/vnd.rip,application/vnd.hbci,application/vnd.hp-jlyt,application/vnd.hp-pcl,application/vnd.hp-hpgl,application/vnd.yamaha.h-script,application/vnd.yamaha.hv-dic,application/vnd.yamaha.hv-voice,application/vnd.hydrostatix.sof-data,application/hyperstudio,application/vnd.hal+xml,text/html,application/vnd.ibm.rights-management,application/vnd.ibm.securecontainer,text/calendar,application/vnd.iccprofile,image/x-icon,application/vnd.igloader,image/ief,application/vnd.immervision-ivp,application/vnd.immervision-ivu,application/reginfo+xml,text/vnd.in3d.3dml,text/vnd.in3d.spot,mode/iges,application/vnd.intergeo,application/vnd.cinderella,application/vnd.intercon.formnet,application/vnd.isac.fcs,application/ipfix,application/pkix-cert,application/pkixcmp,application/pkix-crl,application/pkix-pkipath,applicaion/vnd.insors.igm,application/vnd.ipunplugged.rcprofile,application/vnd.irepository.package+xml,text/vnd.sun.j2me.app-descriptor,application/java-archive,application/java-vm,application/x-java-jnlp-file,application/java-serializd-object,text/x-java-source,java,application/javascript,application/json,application/vnd.joost.joda-archive,video/jpm,image/jpeg,video/jpeg,application/vnd.kahootz,application/vnd.chipnuts.karaoke-mmd,application/vnd.kde.karbon,aplication/vnd.kde.kchart,application/vnd.kde.kformula,application/vnd.kde.kivio,application/vnd.kde.kontour,application/vnd.kde.kpresenter,application/vnd.kde.kspread,application/vnd.kde.kword,application/vnd.kenameaapp,applicatin/vnd.kidspiration,application/vnd.kinar,application/vnd.kodak-descriptor,application/vnd.las.las+xml,application/x-latex,application/vnd.llamagraphics.life-balance.desktop,application/vnd.llamagraphics.life-balance.exchange+xml,application/vnd.jam,application/vnd.lotus-1-2-3,application/vnd.lotus-approach,application/vnd.lotus-freelance,application/vnd.lotus-notes,application/vnd.lotus-organizer,application/vnd.lotus-screencam,application/vnd.lotus-wordro,audio/vnd.lucent.voice,audio/x-mpegurl,video/x-m4v,application/mac-binhex40,application/vnd.macports.portpkg,application/vnd.osgeo.mapguide.package,application/marc,application/marcxml+xml,application/mxf,application/vnd.wolfrm.player,application/mathematica,application/mathml+xml,application/mbox,application/vnd.medcalcdata,application/mediaservercontrol+xml,application/vnd.mediastation.cdkey,application/vnd.mfer,application/vnd.mfmp,model/mesh,appliation/mads+xml,application/mets+xml,application/mods+xml,application/metalink4+xml,application/vnd.ms-powerpoint.template.macroenabled.12,application/vnd.ms-word.document.macroenabled.12,application/vnd.ms-word.template.macroenabed.12,application/vnd.mcd,application/vnd.micrografx.flo,application/vnd.micrografx.igx,application/vnd.eszigno3+xml,application/x-msaccess,video/x-ms-asf,application/x-msdownload,application/vnd.ms-artgalry,application/vnd.ms-ca-compressed,application/vnd.ms-ims,application/x-ms-application,application/x-msclip,image/vnd.ms-modi,application/vnd.ms-fontobject,application/vnd.ms-excel,application/vnd.ms-excel.addin.macroenabled.12,application/vnd.ms-excelsheet.binary.macroenabled.12,application/vnd.ms-excel.template.macroenabled.12,application/vnd.ms-excel.sheet.macroenabled.12,application/vnd.ms-htmlhelp,application/x-mscardfile,application/vnd.ms-lrm,application/x-msmediaview,aplication/x-msmoney,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/vnd.openxmlformats-officedocument.presentationml.slide,application/vnd.openxmlformats-officedocument.presentationml.slideshw,application/vnd.openxmlformats-officedocument.presentationml.template,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.spreadsheetml.template,application/vnd.openxmformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.wordprocessingml.template,application/x-msbinder,application/vnd.ms-officetheme,application/onenote,audio/vnd.ms-playready.media.pya,vdeo/vnd.ms-playready.media.pyv,application/vnd.ms-powerpoint,application/vnd.ms-powerpoint.addin.macroenabled.12,application/vnd.ms-powerpoint.slide.macroenabled.12,application/vnd.ms-powerpoint.presentation.macroenabled.12,appliation/vnd.ms-powerpoint.slideshow.macroenabled.12,application/vnd.ms-project,application/x-mspublisher,application/x-msschedule,application/x-silverlight-app,application/vnd.ms-pki.stl,application/vnd.ms-pki.seccat,application/vn.visio,video/x-ms-wm,audio/x-ms-wma,audio/x-ms-wax,video/x-ms-wmx,application/x-ms-wmd,application/vnd.ms-wpl,application/x-ms-wmz,video/x-ms-wmv,video/x-ms-wvx,application/x-msmetafile,application/x-msterminal,application/msword,application/x-mswrite,application/vnd.ms-works,application/x-ms-xbap,application/vnd.ms-xpsdocument,audio/midi,application/vnd.ibm.minipay,application/vnd.ibm.modcap,application/vnd.jcp.javame.midlet-rms,application/vnd.tmobile-ivetv,application/x-mobipocket-ebook,application/vnd.mobius.mbk,application/vnd.mobius.dis,application/vnd.mobius.plc,application/vnd.mobius.mqy,application/vnd.mobius.msl,application/vnd.mobius.txf,application/vnd.mobius.daf,tex/vnd.fly,application/vnd.mophun.certificate,application/vnd.mophun.application,video/mj2,audio/mpeg,video/vnd.mpegurl,video/mpeg,application/mp21,audio/mp4,video/mp4,application/mp4,application/vnd.apple.mpegurl,application/vnd.msician,application/vnd.muvee.style,application/xv+xml,application/vnd.nokia.n-gage.data,application/vnd.nokia.n-gage.symbian.install,application/x-dtbncx+xml,application/x-netcdf,application/vnd.neurolanguage.nlu,application/vnd.na,application/vnd.noblenet-directory,application/vnd.noblenet-sealer,application/vnd.noblenet-web,application/vnd.nokia.radio-preset,application/vnd.nokia.radio-presets,text/n3,application/vnd.novadigm.edm,application/vnd.novadim.edx,application/vnd.novadigm.ext,application/vnd.flographit,audio/vnd.nuera.ecelp4800,audio/vnd.nuera.ecelp7470,audio/vnd.nuera.ecelp9600,application/oda,application/ogg,audio/ogg,video/ogg,application/vnd.oma.dd2+xml,applicatin/vnd.oasis.opendocument.text-web,application/oebps-package+xml,application/vnd.intu.qbo,application/vnd.openofficeorg.extension,application/vnd.yamaha.openscoreformat,audio/webm,video/webm,application/vnd.oasis.opendocument.char,application/vnd.oasis.opendocument.chart-template,application/vnd.oasis.opendocument.database,application/vnd.oasis.opendocument.formula,application/vnd.oasis.opendocument.formula-template,application/vnd.oasis.opendocument.grapics,application/vnd.oasis.opendocument.graphics-template,application/vnd.oasis.opendocument.image,application/vnd.oasis.opendocument.image-template,application/vnd.oasis.opendocument.presentation,application/vnd.oasis.opendocumen.presentation-template,application/vnd.oasis.opendocument.spreadsheet,application/vnd.oasis.opendocument.spreadsheet-template,application/vnd.oasis.opendocument.text,application/vnd.oasis.opendocument.text-master,application/vnd.asis.opendocument.text-template,image/ktx,application/vnd.sun.xml.calc,application/vnd.sun.xml.calc.template,application/vnd.sun.xml.draw,application/vnd.sun.xml.draw.template,application/vnd.sun.xml.impress,application/vnd.sun.xl.impress.template,application/vnd.sun.xml.math,application/vnd.sun.xml.writer,application/vnd.sun.xml.writer.global,application/vnd.sun.xml.writer.template,application/x-font-otf,application/vnd.yamaha.openscoreformat.osfpvg+xml,application/vnd.osgi.dp,application/vnd.palm,text/x-pascal,application/vnd.pawaafile,application/vnd.hp-pclxl,application/vnd.picsel,image/x-pcx,image/vnd.adobe.photoshop,application/pics-rules,image/x-pict,application/x-chat,aplication/pkcs10,application/x-pkcs12,application/pkcs7-mime,application/pkcs7-signature,application/x-pkcs7-certreqresp,application/x-pkcs7-certificates,application/pkcs8,application/vnd.pocketlearn,image/x-portable-anymap,image/-portable-bitmap,application/x-font-pcf,application/font-tdpfr,application/x-chess-pgn,image/x-portable-graymap,image/png,image/x-portable-pixmap,application/pskc+xml,application/vnd.ctc-posml,application/postscript,application/xfont-type1,application/vnd.powerbuilder6,application/pgp-encrypted,application/pgp-signature,application/vnd.previewsystems.box,application/vnd.pvi.ptid1,application/pls+xml,application/vnd.pg.format,application/vnd.pg.osasli,tex/prs.lines.tag,application/x-font-linux-psf,application/vnd.publishare-delta-tree,application/vnd.pmi.widget,application/vnd.quark.quarkxpress,application/vnd.epson.esf,application/vnd.epson.msf,application/vnd.epson.ssf,applicaton/vnd.epson.quickanime,application/vnd.intu.qfx,video/quicktime,application/x-rar-compressed,audio/x-pn-realaudio,audio/x-pn-realaudio-plugin,application/rsd+xml,application/vnd.rn-realmedia,application/vnd.realvnc.bed,applicatin/vnd.recordare.musicxml,application/vnd.recordare.musicxml+xml,application/relax-ng-compact-syntax,application/vnd.data-vision.rdz,application/rdf+xml,application/vnd.cloanto.rp9,application/vnd.jisp,application/rtf,text/richtex,application/vnd.route66.link66+xml,application/rss+xml,application/shf+xml,application/vnd.sailingtracker.track,image/svg+xml,application/vnd.sus-calendar,application/sru+xml,application/set-payment-initiation,application/set-reistration-initiation,application/vnd.sema,application/vnd.semd,application/vnd.semf,application/vnd.seemail,application/x-font-snf,application/scvp-vp-request,application/scvp-vp-response,application/scvp-cv-request,application/svp-cv-response,application/sdp,text/x-setext,video/x-sgi-movie,application/vnd.shana.informed.formdata,application/vnd.shana.informed.formtemplate,application/vnd.shana.informed.interchange,application/vnd.shana.informed.package,application/thraud+xml,application/x-shar,image/x-rgb,application/vnd.epson.salt,application/vnd.accpac.simply.aso,application/vnd.accpac.simply.imp,application/vnd.simtech-mindmapper,application/vnd.commonspace,application/vnd.ymaha.smaf-audio,application/vnd.smaf,application/vnd.yamaha.smaf-phrase,application/vnd.smart.teacher,application/vnd.svd,application/sparql-query,application/sparql-results+xml,application/srgs,application/srgs+xml,application/sml+xml,application/vnd.koan,text/sgml,application/vnd.stardivision.calc,application/vnd.stardivision.draw,application/vnd.stardivision.impress,application/vnd.stardivision.math,application/vnd.stardivision.writer,application/vnd.tardivision.writer-global,application/vnd.stepmania.stepchart,application/x-stuffit,application/x-stuffitx,application/vnd.solent.sdkm+xml,application/vnd.olpc-sugar,audio/basic,application/vnd.wqd,application/vnd.symbian.install,application/smil+xml,application/vnd.syncml+xml,application/vnd.syncml.dm+wbxml,application/vnd.syncml.dm+xml,application/x-sv4cpio,application/x-sv4crc,application/sbml+xml,text/tab-separated-values,image/tiff,application/vnd.to.intent-module-archive,application/x-tar,application/x-tcl,application/x-tex,application/x-tex-tfm,application/tei+xml,text/plain,application/vnd.spotfire.dxp,application/vnd.spotfire.sfs,application/timestamped-data,applicationvnd.trid.tpt,application/vnd.triscape.mxs,text/troff,application/vnd.Trueapp,application/x-font-ttf,text/turtle,application/vnd.umajin,application/vnd.uoml+xml,application/vnd.unity,application/vnd.ufdl,text/uri-list,application/nd.uiq.theme,application/x-ustar,text/x-uuencode,text/x-vcalendar,text/x-vcard,application/x-cdlink,application/vnd.vsf,model/vrml,application/vnd.vcx,model/vnd.mts,model/vnd.vtu,application/vnd.visionary,video/vnd.vivo,applicatin/ccxml+xml,,application/voicexml+xml,application/x-wais-source,application/vnd.wap.wbxml,image/vnd.wap.wbmp,audio/x-wav,application/davmount+xml,application/x-font-woff,application/wspolicy+xml,image/webp,application/vnd.webturb,application/widget,application/winhlp,text/vnd.wap.wml,text/vnd.wap.wmlscript,application/vnd.wap.wmlscriptc,application/vnd.wordperfect,application/vnd.wt.stf,application/wsdl+xml,image/x-xbitmap,image/x-xpixmap,image/x-xwindowump,application/x-x509-ca-cert,application/x-xfig,application/xhtml+xml,application/xml,application/xcap-diff+xml,application/xenc+xml,application/patch-ops-error+xml,application/resource-lists+xml,application/rls-services+xml,aplication/resource-lists-diff+xml,application/xslt+xml,application/xop+xml,application/x-xpinstall,application/xspf+xml,application/vnd.mozilla.xul+xml,chemical/x-xyz,text/yaml,application/yang,application/yin+xml,application/vnd.ul,application/zip,application/vnd.handheld-entertainment+xml,application/vnd.zzazz.deck+xml')
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.panel.shown", False)
        profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
        profile.set_preference("browser.download.manager.focusWhenStarting", False)
        profile.set_preference("browser.download.manager.useWindow", False)
        profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        profile.set_preference("browser.download.manager.closeWhenDone", True)
        profile.set_preference("pdfjs.disabled", True)

        try:
            driver = webdriver.Firefox(options=options, executable_path=self.gecko_driver, firefox_profile=profile)
        except:
            console.print(f'[red]Unable to create firefox session & Retrying Again!!')
            try:
                driver = webdriver.Firefox(options=options, executable_path=self.gecko_driver, firefox_profile=profile)
            except:
                console.print(f'[red]Unable to create firefox session')
                exit(4)

        #going to page to load session
        driver.get(url)
        # loading cookies
        try:
            cookies = pickle.load(open(self.cookie_path + "pot_cookie.pkl", "rb"))
            for cookie in cookies:
                # adding the cookies to the session through webdriver instance
                if cookie['name'] == "xf_user":
                    driver.add_cookie(cookie)
                #print("Cookie loaded")
        except:
            console.print(f'[red]unable to load cookies')

        # going to home page after loading cookies
        driver.get(url)
        sleep(1)

        # checking if being asked for credentials
        if self.checked_if_url_changed(driver, 'login'):
            console.print(f'[red]logging in using credentials')
            self.login(driver)

        if meta['genres'].__contains__('sport') or (
                str(meta['title']).lower().__contains__('ufc') or str(meta['title']).lower().__contains__('vs')):
            meta['media_type'] = "sport"
        else:
            meta['media_type'] = str(meta['category'])

        #finding and going to the section to upload
        if meta['media_type'].lower().__contains__("movie") and not ("ufc" in meta['title'].lower() or "boxing" in meta['title'].lower() or ("boxing" in meta['keywords'].lower() and "vs" in meta['title'].lower() and ("sport" in meta['keywords'].lower() or "sports" in meta['keywords'].lower()))):
            movie_type_link = self.movie_links[self.identify_type(meta['name'], meta)]
            driver.get(movie_type_link)
            #print(self.message + "Movie Type = " + movie_type_link + "\n" + self.message)
            console.print(f"[yellow]Movie Type = " + movie_type_link)
        else:
            #print(t_name, movie)
            series_type_link = self.tv_links[self.identify_type(meta['name'], meta)]
            driver.get(series_type_link)
            console.print(f"[yellow]TV Type = " + series_type_link)


        common = COMMON(config=self.config)
        await common.edit_torrent(meta, self.tracker, self.source_flag)

        if meta['debug'] == False:
            # setting name and removing .'s
            title = driver.find_element("name", "title")
            title.clear()
            sleep(0.25)
            title.send_keys(meta['name'].replace(':', '').replace("'", ''))

            des = driver.find_element(By.CLASS_NAME, "fr-element.fr-view")
            des.clear()
            try:
                des.send_keys(description)
            except:
                console.print(f'[red]Exception generated when adding description')
                console.print(traceback.print_exc())

            while 1:
                try:
                    e = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                    torrent_file = f"{meta['base_dir']}/tmp/{meta['uuid']}/[{self.tracker}]{meta['clean_name']}.torrent"
                    e.send_keys(torrent_file)
                    break
                except:
                    print()

            # wait till torrent file is uploaded
            sleep(1)
            driver.find_element(By.CLASS_NAME, "button--primary.button.button--icon.button--icon--write").click()


            wait_time = 0
            while not self.check_if_contains(driver, "download"):
                # print(wait_time)
                if wait_time >= 30:
                    print("Page never loaded to dl the torrent file")
                    break
                sleep(1)
                wait_time += 1
            try:
                torrent_file_to_dl = driver.find_element(By.CLASS_NAME, "filename")
            except:
                sleep(10)
                print(driver.page_source)
                torrent_file_to_dl = driver.find_element(By.CLASS_NAME, "filename")
            # print("\ntorrent name = " + movie['name'])
            console.print(f"[green]{driver.current_url}")
            sleep(1)
            torrent_file_to_dl.click()


            await self.add_tracker_torrent(meta, self.tracker, self.source_flag, await self.get_torrent_tracker(meta, self.tracker, self.source_flag), driver.current_url)

        else:
            #cprint(f"description Data:", 'cyan')
            console.print(f"[cyan]description Data:")
            print(description)
        try:
            pickle.dump(driver.get_cookies(), open(self.cookie_path + "pot_cookie.pkl", "wb"))
        except:
            console.print(f"[red]error saving cookie")
        driver.close()


    ### todo
    ###### NEED TO ADD FREELEECH OPTION ###############################

    async def edit_desc(self, movie, tracker):
        heading = "[COLOR=GREEN][size=6]"
        subheading = "[COLOR=RED][size=4]"
        heading_end = "[/size][/COLOR]"
        code_start = "[code]"
        code_end = "[/code]"
        base = open(f"{movie['base_dir']}/tmp/{movie['uuid']}/DESCRIPTION.txt", 'r').read()
        with open(f"{movie['base_dir']}/tmp/{movie['uuid']}/[{tracker}]DESCRIPTION.txt", 'w') as descfile:
            description = ""
            if tracker == "POTUK":
                if movie['poster'] is not None:
                    description += '[IMG width="640px"]' + movie['poster'] + "[/IMG] \n\n"
            description += heading + str(movie['name']) + heading_end + "\n\n" + "\n\n"
            if movie['is_disc'] != 'BDMV':
                description += subheading + "MEDIA INFO" + heading_end + "\n"
                # Beautify MediaInfo for HDT using custom template
                video = movie['filelist'][0]
                mi_template = os.path.abspath(f"{movie['base_dir']}/data/templates/MEDIAINFO.txt")
                if os.path.exists(mi_template):
                    media_info = MediaInfo.parse(video, output="STRING", full=False,
                                                 mediainfo_options={"inform": f"file://{mi_template}"})
                    description += (f"""\n{media_info}\n[/code]\n""")
                else:
                    console.print("[bold red]Couldn't find the MediaInfo template")
                    console.print("[green]Using normal MediaInfo for the description.")

                    with open(f"{movie['base_dir']}/tmp/{movie['uuid']}/MEDIAINFO_CLEANPATH.txt", 'r',
                              encoding='utf-8') as MI:
                        description += (f"""[code]\n{MI.read()}\n[/code]\n\n""")
            else:
                description += subheading + "DISC INFO" + heading_end + "\n"
                with open(f"{movie['base_dir']}/tmp/{movie['uuid']}/BD_SUMMARY_00.txt", 'r',
                          encoding='utf-8') as BD_SUMMARY:
                    description += (f"""[code]\n{BD_SUMMARY.read()}\n[/code]\n\n""")

            description += "\n\n" + subheading + "PLOT" + heading_end + "\n" + str(movie['overview'])
            if movie['genres']:
                description += "\n\n" + subheading + "Genres" + heading_end + "\n" + str(movie['genres'])

            description += self.get_links(movie, subheading, heading_end)
            if movie['image_list'] is not None:
                description += "\n\n" + subheading + "Screenshots" + heading_end + "\n"
                for image in movie['image_list']:
                    if image['raw_url'] != None:
                        if tracker.lower().__contains__("pot"):
                            description += '[IMG width="250px"]' + image['raw_url'] + "[/IMG]"
                        else:
                            # not possible to resize images on AR or HDS
                            if 'th_url' in image:
                                description += "[url=" + image['raw_url'] + "][img]" + image['th_url'] + "[/img][/url]"
                            else:
                                description += "[url=" + image['raw_url'] + "][img]" + image['img_url'] + "[/img][/url]"
            if 'youtube' in movie:
                description += "\n\n" + subheading + "Youtube" + heading_end + "\n" + str(movie['youtube'])

            #adding extra description if passed
            if len(base) > 2:
                description += "\n\n" + subheading + "Notes" + heading_end + "\n" + str(base)

            descfile.write(description)
            descfile.close()
        return

    def get_links(self, movie, subheading, heading_end):
        description = ""
        description += "\n\n" + subheading + "Links" + heading_end + "\n"
        if movie['imdb_id'] != "0":
            description += f"[URL=https://www.imdb.com/title/tt{movie['imdb_id']}][img]{self.config['IMAGES']['imdb_75']}[/img][/URL]"
        if movie['tmdb'] != "0":
            description += f" [URL=https://www.themoviedb.org/{str(movie['category'].lower())}/{str(movie['tmdb'])}][img]{self.config['IMAGES']['tmdb_75']}[/img][/URL]"
        if movie['tvdb_id'] != 0:
            description += f" [URL=https://www.thetvdb.com/?id={str(movie['tvdb_id'])}&tab=series][img]{self.config['IMAGES']['tvdb_75']}[/img][/URL]"
        if movie['tvmaze_id'] != 0:
            description += f" [URL=https://www.tvmaze.com/shows/{str(movie['tvmaze_id'])}][img]{self.config['IMAGES']['tvmaze_75']}[/img][/URL]"
        if movie['mal_id'] != 0:
            description += f" [URL=https://myanimelist.net/anime/{str(movie['mal_id'])}][img]{self.config['IMAGES']['mal_75']}[/img][/URL]"
        return description

    # this tracker has uique passkeys for each torrent so torrent has to be dl to add to client.
    async def add_tracker_torrent(self, meta, tracker, source_flag, new_tracker, comment):
        if os.path.exists(f"{meta['base_dir']}/tmp/{meta['uuid']}/BASE.torrent"):
            new_torrent = Torrent.read(f"{meta['base_dir']}/tmp/{meta['uuid']}/BASE.torrent")
            new_torrent.metainfo['announce'] = new_tracker
            new_torrent.metainfo['comment'] = comment
            new_torrent.metainfo['info']['source'] = source_flag
            Torrent.copy(new_torrent).write(f"{meta['base_dir']}/tmp/{meta['uuid']}/[{tracker}]{meta['clean_name']}.torrent", overwrite=True)

    async def get_torrent_tracker(self, meta, tracker, source_flag):
        if os.path.exists(f"{meta['base_dir']}/tmp/{meta['uuid']}/[{tracker}]{meta['clean_name']} [PotUK.net].torrent"):
            new_torrent = Torrent.read(f"{meta['base_dir']}/tmp/{meta['uuid']}/[{tracker}]{meta['clean_name']} [PotUK.net].torrent")
            return new_torrent.metainfo['announce']
        else:
            sleep(5)
            if os.path.exists(
                    f"{meta['base_dir']}/tmp/{meta['uuid']}/[{tracker}]{meta['clean_name']} [PotUK.net].torrent"):
                new_torrent = Torrent.read(
                    f"{meta['base_dir']}/tmp/{meta['uuid']}/[{tracker}]{meta['clean_name']} [PotUK.net].torrent")
                return new_torrent.metainfo['announce']
            else:
                print("tracker did not download")

    # using jackett to search for dupes
    async def search_existing(self, meta, tracker_code):
        api_key = self.config['JACKET'].get('api_key')
        j_url = self.config['JACKET'].get('url')

        dupes = []
        console.print(f"[yellow]Searching for existing torrents on site...")
        what = ""
        #adding title to search
        what = unquote(meta['title'].replace(':', '').replace("'", '').replace(",", ''))
        if meta['tv_pack']:
            what += " " + meta['season']
        else:
            what += " " + meta['season'] + meta['episode']

        params = [
            ('apikey', api_key),
            ('q', what),
            ('cache', 'false')
        ]
        # if category is not None:
        #     params.append(('cat', ','.join(category)))
        for k in what.replace("'", "").split("\n"):
            what = re.sub(r"[^a-zA-Z0-9]+", ' ', k).replace('.', " ")
        console.print(f"[yellow]Searching for " + what)
        params = urlencode(params)
        jacket_url = j_url + "/api/v2.0/indexers/" + tracker_code + "/results/torznab/api?%s" % params

        try:
            response = self.get_response(jacket_url)
            if response is not None:
                # process search results
                response_xml = xml.etree.ElementTree.fromstring(response)
                for each in response_xml.find('channel').findall('item'):
                    res = {}

                    result = each.find('title').text
                    #print(result)
                    # print(result)
                    difference = SequenceMatcher(None, meta['clean_name'].replace('DD+', 'DDP'), result).ratio()
                    if difference >= 0.05:
                        dupes.append(result)
            else:
                if 'status_message' in response:
                    console.print(f"[yellow]{response.get('status_message')}")
                    await asyncio.sleep(5)
                else:
                    console.print(f"[red]Site Seems to be down or not responding to API")
        except:
            console.print(f"[red]Unable to search for existing torrents on site. Most likely the site is down or Jackett is down.")
            dupes.append("FAILED SEARCH")
            print(traceback.print_exc())
            await asyncio.sleep(5)

        return dupes

    def get_response(self, query):
        response = None
        try:
            # we can't use helpers.retrieve_url because of redirects
            # we need the cookie processor to handle redirects
            opener = urllib_request.build_opener(urllib_request.HTTPCookieProcessor(CookieJar()))
            response = opener.open(query).read().decode('utf-8')
        except urllib_request.HTTPError as e:
            # if the page returns a magnet redirect, used in download_torrent
            if e.code == 302:
                response = e.url
        except Exception:
            pass
        return response