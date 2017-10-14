
from matplotlib.colors import ListedColormap
from numpy import nan, inf

# Used to reconstruct the colormap in pycam02ucs.cm.viscm
parameters = {'xp': [16.121891585344997, 33.901145962549492, 5.5873058066040926, -14.703203914141397, -17.875928056390336, -5.3288735306278738],
              'yp': [-2.5423728813559308, -13.425925925925895, -42.422027290448327, -35.333333333333314, -8.83264462809916, -2.1686159844054487],
              'min_Jp': 15.0,
              'max_Jp': 95.0}

cm_data = [[ 0.21298394, 0.05589169, 0.14220951],
           [ 0.21780744, 0.0570005 , 0.14665582],
           [ 0.22261214, 0.05808842, 0.15115908],
           [ 0.22739756, 0.05915624, 0.15572185],
           [ 0.23216536, 0.06020099, 0.16034977],
           [ 0.23691745, 0.06121879, 0.1650498 ],
           [ 0.24164654, 0.06222163, 0.169816  ],
           [ 0.24635153, 0.06321115, 0.17465056],
           [ 0.25103114, 0.06418929, 0.1795555 ],
           [ 0.25568737, 0.06515168, 0.1845388 ],
           [ 0.26031556, 0.06610638, 0.18959733],
           [ 0.26491272, 0.06705861, 0.19473015],
           [ 0.26947709, 0.0680114 , 0.19993831],
           [ 0.27400681, 0.06896804, 0.20522255],
           [ 0.27849993, 0.06993211, 0.21058327],
           [ 0.28295501, 0.07090603, 0.21602205],
           [ 0.28737014, 0.0718934 , 0.22153921],
           [ 0.29174204, 0.07290112, 0.22713094],
           [ 0.29606871, 0.07393344, 0.23279613],
           [ 0.30034822, 0.07499465, 0.23853326],
           [ 0.30457867, 0.07608911, 0.24434046],
           [ 0.30875826, 0.07722111, 0.25021549],
           [ 0.31288529, 0.0783949 , 0.25615575],
           [ 0.3169582 , 0.07961456, 0.26215837],
           [ 0.32097556, 0.08088399, 0.26822019],
           [ 0.32493609, 0.08220684, 0.27433782],
           [ 0.3288387 , 0.08358647, 0.28050768],
           [ 0.33268245, 0.08502593, 0.28672608],
           [ 0.33646657, 0.08652789, 0.2929892 ],
           [ 0.34019047, 0.08809468, 0.29929318],
           [ 0.34385372, 0.08972821, 0.30563417],
           [ 0.34745604, 0.09143006, 0.31200825],
           [ 0.35099729, 0.0932014 , 0.31841152],
           [ 0.35447749, 0.09504303, 0.32484029],
           [ 0.35789677, 0.09695535, 0.33129096],
           [ 0.36125536, 0.09893846, 0.33776007],
           [ 0.36455362, 0.10099212, 0.34424427],
           [ 0.36779195, 0.10311585, 0.35074041],
           [ 0.37097085, 0.10530889, 0.35724546],
           [ 0.37409088, 0.10757029, 0.36375657],
           [ 0.37715263, 0.10989888, 0.37027108],
           [ 0.38015674, 0.11229336, 0.37678646],
           [ 0.38310387, 0.11475229, 0.38330035],
           [ 0.38599472, 0.11727411, 0.38981058],
           [ 0.38882999, 0.1198572 , 0.3963151 ],
           [ 0.39161037, 0.12249987, 0.402812  ],
           [ 0.3943366 , 0.12520039, 0.40929955],
           [ 0.39700936, 0.12795703, 0.41577611],
           [ 0.39962936, 0.13076802, 0.42224018],
           [ 0.40219729, 0.13363161, 0.42869038],
           [ 0.40471394, 0.13654614, 0.43512488],
           [ 0.40717995, 0.13950986, 0.44154258],
           [ 0.4095959 , 0.14252107, 0.44794287],
           [ 0.41196239, 0.14557814, 0.45432475],
           [ 0.41428002, 0.1486795 , 0.4606873 ],
           [ 0.41654936, 0.15182361, 0.46702967],
           [ 0.41877098, 0.15500903, 0.47335108],
           [ 0.4209454 , 0.15823432, 0.4796508 ],
           [ 0.42307313, 0.16149814, 0.48592814],
           [ 0.42515465, 0.16479918, 0.49218247],
           [ 0.42719043, 0.1681362 , 0.49841321],
           [ 0.42918111, 0.17150798, 0.50461925],
           [ 0.431127  , 0.17491341, 0.5108004 ],
           [ 0.43302838, 0.17835141, 0.5169565 ],
           [ 0.43488561, 0.18182099, 0.52308708],
           [ 0.43669905, 0.18532117, 0.5291917 ],
           [ 0.43846903, 0.18885105, 0.53526994],
           [ 0.44019583, 0.19240976, 0.54132138],
           [ 0.44187976, 0.19599648, 0.54734563],
           [ 0.44352106, 0.19961045, 0.5533423 ],
           [ 0.44512012, 0.2032509 , 0.55931077],
           [ 0.44667705, 0.20691717, 0.56525088],
           [ 0.44819199, 0.21060865, 0.57116243],
           [ 0.44966511, 0.21432473, 0.57704502],
           [ 0.45109659, 0.21806485, 0.58289828],
           [ 0.45248658, 0.22182847, 0.58872183],
           [ 0.45383521, 0.2256151 , 0.59451528],
           [ 0.45514261, 0.22942427, 0.60027826],
           [ 0.45640887, 0.23325554, 0.60601037],
           [ 0.45763398, 0.23710854, 0.61171135],
           [ 0.45881803, 0.24098289, 0.61738074],
           [ 0.4599611 , 0.24487823, 0.62301809],
           [ 0.46106323, 0.24879421, 0.62862296],
           [ 0.46212445, 0.25273054, 0.63419487],
           [ 0.46314479, 0.25668693, 0.63973335],
           [ 0.46412426, 0.2606631 , 0.6452379 ],
           [ 0.46506286, 0.2646588 , 0.650708  ],
           [ 0.46596031, 0.26867393, 0.65614343],
           [ 0.46681665, 0.27270825, 0.66154354],
           [ 0.467632  , 0.27676148, 0.66690758],
           [ 0.46840632, 0.28083345, 0.67223496],
           [ 0.46913959, 0.28492398, 0.67752502],
           [ 0.46983176, 0.28903289, 0.68277713],
           [ 0.47048281, 0.29316004, 0.68799058],
           [ 0.4710927 , 0.29730529, 0.69316468],
           [ 0.47166137, 0.30146848, 0.69829868],
           [ 0.47218867, 0.30564956, 0.70339194],
           [ 0.47267406, 0.30984863, 0.70844403],
           [ 0.47311806, 0.3140653 , 0.71345366],
           [ 0.47352067, 0.31829946, 0.71841996],
           [ 0.47388188, 0.322551  , 0.72334205],
           [ 0.47420168, 0.32681981, 0.728219  ],
           [ 0.47448009, 0.33110575, 0.73304987],
           [ 0.47471715, 0.33540873, 0.73783366],
           [ 0.4749129 , 0.33972863, 0.74256938],
           [ 0.47506742, 0.34406531, 0.74725597],
           [ 0.4751808 , 0.34841867, 0.75189235],
           [ 0.47525316, 0.35278857, 0.75647742],
           [ 0.47528466, 0.35717487, 0.76101004],
           [ 0.47527514, 0.36157758, 0.76548918],
           [ 0.47522479, 0.36599656, 0.76991363],
           [ 0.47513427, 0.37043147, 0.77428199],
           [ 0.47500393, 0.37488213, 0.77859297],
           [ 0.47483412, 0.37934834, 0.7828453 ],
           [ 0.4746253 , 0.38382989, 0.78703766],
           [ 0.47437795, 0.38832654, 0.7911687 ],
           [ 0.47409263, 0.39283807, 0.79523708],
           [ 0.47376999, 0.39736419, 0.79924139],
           [ 0.47341074, 0.40190463, 0.80318024],
           [ 0.47301567, 0.40645908, 0.80705223],
           [ 0.47258566, 0.41102721, 0.81085591],
           [ 0.47212171, 0.41560865, 0.81458986],
           [ 0.4716249 , 0.42020304, 0.81825263],
           [ 0.47109642, 0.42480997, 0.82184277],
           [ 0.47053758, 0.42942898, 0.82535887],
           [ 0.4699498 , 0.43405962, 0.82879947],
           [ 0.46933466, 0.43870139, 0.83216318],
           [ 0.46869383, 0.44335376, 0.83544858],
           [ 0.46802917, 0.44801616, 0.83865432],
           [ 0.46734263, 0.45268799, 0.84177905],
           [ 0.46663636, 0.45736864, 0.84482148],
           [ 0.46591265, 0.46205743, 0.84778034],
           [ 0.46517394, 0.46675366, 0.85065444],
           [ 0.46442285, 0.47145661, 0.85344263],
           [ 0.46366216, 0.4761655 , 0.85614385],
           [ 0.46289481, 0.48087955, 0.85875708],
           [ 0.46212297, 0.48559831, 0.8612812 ],
           [ 0.4613509 , 0.49032052, 0.86371555],
           [ 0.46058208, 0.49504528, 0.86605942],
           [ 0.45982017, 0.49977167, 0.86831217],
           [ 0.45906898, 0.50449872, 0.87047333],
           [ 0.4583325 , 0.50922545, 0.87254251],
           [ 0.45761487, 0.51395086, 0.87451947],
           [ 0.45692037, 0.51867392, 0.87640412],
           [ 0.45625342, 0.52339359, 0.87819649],
           [ 0.45561856, 0.52810881, 0.87989676],
           [ 0.45502044, 0.53281852, 0.88150529],
           [ 0.45446291, 0.53752203, 0.8830221 ],
           [ 0.45395166, 0.5422179 , 0.88444824],
           [ 0.45349173, 0.54690499, 0.88578463],
           [ 0.45308803, 0.55158223, 0.88703226],
           [ 0.45274551, 0.55624857, 0.8881923 ],
           [ 0.45246908, 0.56090297, 0.88926607],
           [ 0.45226366, 0.5655444 , 0.89025507],
           [ 0.45213406, 0.57017185, 0.89116092],
           [ 0.45208461, 0.57478456, 0.89198505],
           [ 0.45212047, 0.57938135, 0.89272981],
           [ 0.45224622, 0.5839613 , 0.89339735],
           [ 0.45246621, 0.58852353, 0.89398987],
           [ 0.45278458, 0.59306722, 0.89450974],
           [ 0.45320531, 0.59759159, 0.89495941],
           [ 0.45373211, 0.60209592, 0.89534144],
           [ 0.45436847, 0.60657953, 0.8956585 ],
           [ 0.45511768, 0.61104174, 0.89591342],
           [ 0.45598269, 0.61548199, 0.89610905],
           [ 0.45696613, 0.61989976, 0.89624827],
           [ 0.45807033, 0.62429458, 0.89633399],
           [ 0.45929732, 0.62866605, 0.89636919],
           [ 0.46064879, 0.63301382, 0.89635684],
           [ 0.46212629, 0.6373375 , 0.89630027],
           [ 0.46373081, 0.6416369 , 0.89620239],
           [ 0.46546305, 0.64591186, 0.89606608],
           [ 0.46732345, 0.65016224, 0.89589433],
           [ 0.46931216, 0.65438798, 0.89569008],
           [ 0.47142903, 0.65858902, 0.89545627],
           [ 0.47367364, 0.66276538, 0.89519579],
           [ 0.47604536, 0.66691708, 0.89491161],
           [ 0.47854335, 0.67104413, 0.89460702],
           [ 0.48116628, 0.67514678, 0.89428415],
           [ 0.48391278, 0.67922522, 0.89394566],
           [ 0.48678129, 0.68327963, 0.89359417],
           [ 0.48977007, 0.68731025, 0.89323218],
           [ 0.4928772 , 0.69131735, 0.89286215],
           [ 0.49610063, 0.69530122, 0.89248647],
           [ 0.49943822, 0.69926217, 0.89210744],
           [ 0.50288765, 0.70320047, 0.89172772],
           [ 0.50644655, 0.70711649, 0.89134936],
           [ 0.51011248, 0.71101066, 0.8909741 ],
           [ 0.51388294, 0.71488334, 0.89060393],
           [ 0.51775541, 0.71873493, 0.89024078],
           [ 0.52172732, 0.72256583, 0.8898865 ],
           [ 0.5257961 , 0.72637645, 0.88954287],
           [ 0.52995915, 0.7301672 , 0.8892116 ],
           [ 0.53421391, 0.7339385 , 0.88889434],
           [ 0.5385578 , 0.73769077, 0.88859267],
           [ 0.5429883 , 0.74142444, 0.88830811],
           [ 0.54750281, 0.74513991, 0.88804246],
           [ 0.5520989 , 0.74883762, 0.88779685],
           [ 0.55677422, 0.75251799, 0.88757251],
           [ 0.56152638, 0.75618144, 0.88737072],
           [ 0.56635309, 0.75982839, 0.88719273],
           [ 0.57125208, 0.76345922, 0.88703974],
           [ 0.57622118, 0.76707435, 0.8869129 ],
           [ 0.58125826, 0.77067417, 0.88681333],
           [ 0.58636126, 0.77425906, 0.88674212],
           [ 0.59152819, 0.7778294 , 0.88670031],
           [ 0.59675713, 0.78138555, 0.88668891],
           [ 0.60204624, 0.78492789, 0.88670892],
           [ 0.60739371, 0.78845676, 0.88676131],
           [ 0.61279785, 0.79197249, 0.886847  ],
           [ 0.61825699, 0.79547544, 0.88696697],
           [ 0.62376953, 0.79896592, 0.88712212],
           [ 0.62933401, 0.80244424, 0.88731328],
           [ 0.63494897, 0.80591071, 0.88754133],
           [ 0.64061303, 0.80936562, 0.88780715],
           [ 0.64632485, 0.81280925, 0.88811162],
           [ 0.65208315, 0.81624189, 0.88845562],
           [ 0.65788673, 0.81966379, 0.88884001],
           [ 0.6637344 , 0.82307522, 0.88926568],
           [ 0.66962506, 0.82647642, 0.88973352],
           [ 0.67555762, 0.82986764, 0.89024441],
           [ 0.68153106, 0.83324911, 0.89079928],
           [ 0.68754438, 0.83662105, 0.89139904],
           [ 0.69359663, 0.83998369, 0.89204464],
           [ 0.69968688, 0.84333724, 0.89273702],
           [ 0.70581423, 0.84668191, 0.89347718],
           [ 0.71197782, 0.85001791, 0.8942661 ],
           [ 0.7181769 , 0.85334541, 0.89510469],
           [ 0.72441053, 0.85666464, 0.89599414],
           [ 0.73067788, 0.8599758 , 0.89693553],
           [ 0.73697811, 0.8632791 , 0.89793   ],
           [ 0.74331039, 0.86657473, 0.89897869],
           [ 0.74967389, 0.86986292, 0.90008279],
           [ 0.75606778, 0.87314387, 0.90124351],
           [ 0.76249117, 0.87641781, 0.90246212],
           [ 0.7689432 , 0.87968498, 0.90373988],
           [ 0.77542295, 0.88294564, 0.9050781 ],
           [ 0.78192947, 0.88620003, 0.90647814],
           [ 0.78846179, 0.88944845, 0.90794134],
           [ 0.79501887, 0.89269119, 0.9094691 ],
           [ 0.80159965, 0.89592859, 0.91106281],
           [ 0.80820295, 0.899161  , 0.91272391],
           [ 0.81482754, 0.90238881, 0.91445386],
           [ 0.82147215, 0.90561245, 0.91625407],
           [ 0.82813543, 0.90883237, 0.91812595],
           [ 0.83481598, 0.91204906, 0.92007088],
           [ 0.84151229, 0.91526306, 0.92209023],
           [ 0.84822279, 0.91847494, 0.92418529],
           [ 0.85494584, 0.92168533, 0.92635732],
           [ 0.8616797 , 0.9248949 , 0.92860749],
           [ 0.86842255, 0.92810438, 0.9309369 ],
           [ 0.87517248, 0.93131455, 0.93334654],
           [ 0.88192751, 0.93452625, 0.93583728],
           [ 0.88868558, 0.93774038, 0.93840987],
           [ 0.89544454, 0.94095789, 0.94106488],
           [ 0.90220216, 0.9441798 , 0.94380273]]

test_cm = ListedColormap(cm_data, name=__file__)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        from viscm import viscm
        viscm(test_cm)
    except ImportError:
        print("viscm not found, falling back on simple display")
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',
                   cmap=test_cm)
    plt.show()
