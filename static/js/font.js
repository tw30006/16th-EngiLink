import { library, dom, config } from "@fortawesome/fontawesome-svg-core";
import { faLocationDot } from '@fortawesome/free-solid-svg-icons';
import { faSackDollar } from '@fortawesome/free-solid-svg-icons';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import { faFire } from '@fortawesome/free-solid-svg-icons';
import { faHeart } from '@fortawesome/free-solid-svg-icons';
import { faBriefcase } from '@fortawesome/free-solid-svg-icons';
import { faThumbsUp } from '@fortawesome/free-regular-svg-icons';

config.mutateApproach = "sync";
library.add(faLocationDot, faSackDollar,faBars,faFire,faHeart,faBriefcase,faThumbsUp);

dom.watch();


